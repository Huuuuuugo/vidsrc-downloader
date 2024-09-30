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

    # wait for the browser to close
    browser_pid = driver.service.process.pid
    while psutil.pid_exists(browser_pid):
        time.sleep(0.5)
    
    return meta_dict


if __name__ == "__main__":
    from pprint import pprint
    output = get_meta_m3u8("https://vidsrc.net/embed/tv?imdb=tt3559912&season=1&episode=1")

    pprint(output)