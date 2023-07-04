import sys
sys.path.append("/home/anthony/Documents/Doctorat/PROD/FELIX/CODE/GPM")
import requests 
from datetime import date, timedelta
import numpy as np 
import os 
import subprocess
import time
import multiprocessing
import random
import glob
import configparser


#https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+Python
# overriding requests.Session.rebuild_auth to mantain headers when redirected

class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'
    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)
 
   # Overrides from the library to keep headers when redirected to or from
   # the NASA auth host.
    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url
        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)
            if (original_parsed.hostname != redirect_parsed.hostname) and \
                    redirect_parsed.hostname != self.AUTH_HOST and \
                    original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
        return
 

# Get username and password from the config.def file
config=configparser.ConfigParser()
config.read("config.def")
username=config.get("OverAll", "username")
password=config.get("OverAll", "password")
#session = SessionWithHeaderRedirection(username, password)
temp_dir=config.get("OverAll", "temp_dir")


def download(url):
    t0 = time.time()
    filename = url[url.rfind('/')+1:] 
    
    if not os.path.isfile(temp_dir+"/"+filename):
        print(filename)
        session = SessionWithHeaderRedirection(username, password)
        try:
          time.sleep(1)
          response = session.get(url)
          response.raise_for_status()
          f = open(filename,'wb')
          f.write(response.content)
          f.close()    
          response.close()
        except requests.exceptions.ConnectionError:
          try:
             response.close()
             session.close()
          except:
             session.close()
             time.sleep(2)
        except:
           print('requests.get() returned an error code '+str(response.status_code))
           try:
               response.close()
               session.close()
           except:
               session.close()
               time.sleep(2)  
        session.close()
          
          
########################################

import calendar

def get_number_of_days(year, month):
    days = calendar.monthrange(year, int(month))[1]
    return days

    
########################################

def get_DD_urls_day(year, month):
    ndays = get_number_of_days(year, month)
    # 

    basic_url = "https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDF.06/{0}/{1:02}/3B-DAY.MS.MRG.3IMERG.{0}{1:02}{2:02}-S000000-E235959.V06.nc4"
    
    L = [basic_url.format(year, month, d) for d in np.arange(1, ndays+1)]
    return L


########################################


def remove_thing(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

def empty_directory(path):
    for i in glob.glob(os.path.join(path, '*')):
        remove_thing(i)

