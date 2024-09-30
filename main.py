import os
import re

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import seleniumwire.undetected_chromedriver as uc


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
        print("######################## MATCH #########################")
        print(request.url)
        print()
        print(request.headers.as_string())
        print("######################## MATCH #########################")

        driver.quit()

driver = uc.Chrome(service = service, options = options, version_main = 129)
driver.request_interceptor = interceptor

driver.get("https://vidsrc.net/embed/tv?imdb=tt3559912&season=1&episode=1")

input("Press Enter to exit")