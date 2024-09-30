import re

from downloader import Download

with open("index-2.m3u8") as playlist:
    for url in playlist:
        url = url.strip()
        if not re.match(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", url):
            continue

        file_name = f"temp/{re.findall(r".*/(.+)\.", url)[0]}.mp4"
        print(file_name)

        headers = {
            "Host": "stat3.datadynamo3.link",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://ate60vs7zcjhsjo5qgv8.com/",
            "Origin": "https://ate60vs7zcjhsjo5qgv8.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site"
        }


        try:
            download = Download(url, file_name, headers)
            download.start()
            download.wait_downloads()

        except Exception as e:
            print(e)
            input()