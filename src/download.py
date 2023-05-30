from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
import os
import time

###################

class chrome_driver:
    """
    Class to download data from the Google Cloud.
    """
    def __init__(self, dir_out):
        """
        Initialization.
        
        Input:
        - dir_out: directory where the file should be downloaded.
        """
        self.options=ChromeOptions()
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": dir_out, 
                 "directory_upgrade": True}
        self.dir_out = dir_out
        self.options.add_experimental_option("prefs", prefs)


    def download(self, year, month):
        """
        Download the file for a specific month, year.
        
        Inputs:
        - month
        - year
        """
        # get the corresponding url
        url = self.get_url(year, month)
        
        # check if file already downloaded
        if os.path.exists(self.dir_out + url.split("/")[-1]):
            return
        
        # launch chrome driver
        driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options = self.options
            )
        
        # open the page
        driver.get(url)
        # while not downloaded, wait
        while not os.path.exists(self.dir_out + url.split("/")[-1]):
            time.sleep(2) 
        driver.close()

    def get_url(self, year, month):
        """
        Get the url of the file corresponding to a specific month.
        
        Inputs:
        - month
        - year
        """
        my_url = f"https://storage.googleapis.com/earthenginepartners-hansen/water/individualMonthMaps/30S_070W/{year}_{month:02d}_percent.tif"
        return my_url
