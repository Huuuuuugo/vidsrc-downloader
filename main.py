import subprocess
import time
import os
import re

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psutil

from downloader import Download

def get_headers_dict(headers_str: str):
    headers_list = headers_str.split('\n')
    headers_dict = {}

    for header in headers_list:
        matches = re.findall(r"(.+?):(.+)", header)
        if matches:
            key = matches[0][0].strip()
            value = matches[0][1].strip()

            headers_dict.update({key: value})
    
    return headers_dict

def get_meta_m3u8(url: str):
    meta_dict = {
        "title": None,
        "url": None,
        "headers": None,
    }
    options = Options()
    options.add_argument('--headless')

    # portable setup
    service = Service(f"{os.getcwd()}\\GoogleChromePortable\\GoogleChromePortable.exe")
    options.binary_location = f"{os.getcwd()}\\GoogleChromePortable\\App\\Chrome-bin\\chrome.exe"
    # options.add_argument(f"--user-data-dir='{os.getcwd()}\\GoogleChromePortable\\Data\\profile'")

    # allow selenium wire to listen
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    # intercept requests
    # blocks unwanted requests and close the browser when the target is found
    def interceptor(request):
        if re.search(r'.*devtool.*', request.url):
            request.abort()

        if re.match(r"^.*master\.m3u8$", request.url):
            meta_dict["url"] = request.url
            meta_dict["headers"] = get_headers_dict(request.headers.as_string())

            driver.quit()

    try:
        driver = uc.Chrome(service = service, options = options, version_main = 129)
        driver.request_interceptor = interceptor

        driver.get(url)

        # wait for obstructing element to appear and then remove it
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dontfoid"))
        )
        driver.execute_script("document.getElementById('dontfoid').remove();")

        # switch to player iframe
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "player_iframe"))
        )
        driver.switch_to.frame(iframe)

        # get title of the video
        title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "iframe_title"))
        )
        meta_dict["title"] = title.text

        # click the play button
        play_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pl_but"))
        )
        play_btn.click()
    
    except Exception as e:
        print(e)
        driver.quit()

    finally:
        # wait for the browser to close
        browser_pid = driver.service.process.pid
        while psutil.pid_exists(browser_pid):
            time.sleep(0.5)
        
        return meta_dict

def download_m3u8_files(meta_dict: dict, output_dir: str = ''):
    if output_dir[-1] not in ('/', '\\'):
        output_dir += '/'

    Download(meta_dict['url'], f"{output_dir}master.m3u8", meta_dict['headers']).start()
    Download.wait_downloads()

    parts_urls = []
    with open(f"{output_dir}master.m3u8", 'r') as meta_file:
        for url in meta_file:
            url = url.strip()
            if re.match(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", url):
                parts_urls.append(url)

    index = 1
    for url in parts_urls:
        try:
            download = Download(url, f"{output_dir}index-{index}.m3u8", meta_dict['headers'])
            download.start()
            Download.wait_downloads()
        
        except Exception as e:
            print(e)
            # TODO FIXME: update downloader to remove object from list when finished or when exception is raised
            if Download.download_list:
                Download.download_list.pop()
        
        finally:
            index+=1

def download_parts(m3u8_path: str, headers: dict, output_dir: str = ''):
    if output_dir[-1] not in ('/', '\\'):
        output_dir += '/'
    
    os.makedirs(f"{output_dir}parts")

    try:
        with open(m3u8_path) as playlist:
            for url in playlist:
                url = url.strip()
                if not re.match(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", url):
                    continue

                file_name = f"{output_dir}parts/{re.findall(r".*/(.+)\.", url)[0]}.mp4"
                print(file_name)

                download = Download(url, file_name, headers)
                download.start()
            
        Download.wait_downloads(False)
    
    finally:
        Download.stop_all()
        # TODO FIXME: update downloader to remove object from list when finished or when exception is raised
        Download.download_list.clear()
    
def concat(input_dir: str, output_file: str):
    if input_dir[-1] not in ('/', '\\'):
        input_dir += '/'

    # create function to properly order the files inside the given directory
    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(0)) if match else 0

    # get files list and order them
    parts = os.listdir(input_dir)
    parts = sorted(parts, key=extract_number)

    # create a file with instructions for ffmpeg
    playlist = [f"file '{os.path.abspath(input_dir)}/{part}'\n".replace('\\', '/') for part in parts]
    with open(f"{input_dir}playlist.txt", 'w') as output:
        output.writelines(playlist)

    # run ffmpeg to concatenate files
    print(os.getcwd())
    subprocess.run(["ffmpeg", 
                    "-f", "concat",
                    "-safe", "0", 
                    "-i", f"{input_dir}playlist.txt", 
                    "-c", "copy", f"{output_file}"
                    ])

    # delete instructions file
    os.remove(f"{input_dir}playlist.txt")


if __name__ == "__main__":
    meta_info = get_meta_m3u8("https://vidsrc.net/embed/tv?imdb=tt3559912&season=1&episode=1")

    download_m3u8_files(meta_info, "temp")

    #TODO: add option to choose resolution
    try:
        download_parts('temp/index-2.m3u8', meta_info['headers'], 'temp')
    
    except Exception as e:
        download_parts('temp/index-1.m3u8', meta_info['headers'], 'temp')

    concat('temp/parts/', '1x1.mp4')