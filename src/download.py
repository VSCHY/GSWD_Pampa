from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
import os
import time

###################

class chrome_driver:
    def __init__(self, dir_out):
        self.options=ChromeOptions()
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": dir_out, 
                 "directory_upgrade": True}
        self.dir_out = dir_out
        self.options.add_experimental_option("prefs", prefs)

    def download(self, year, month):
        driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options = self.options
            )
        url = self.get_url(year, month)
        driver.get(url)
        while not os.path.exists(self.dir_out + url.split("/")[-1]):
            time.sleep(2) 
        driver.close()

    def get_url(self, year, month):
        my_url = f"https://storage.googleapis.com/earthenginepartners-hansen/water/individualMonthMaps/30S_070W/{year}_{month:02d}_percent.tif"
        return my_url
