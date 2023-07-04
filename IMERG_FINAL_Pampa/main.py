import sys
import requests 
from datetime import date, timedelta
import numpy as np 
import os 
import subprocess
import time
import multiprocessing
import random
import glob
import download_function as down
from calendar import monthrange
import configparser
import xarray as xr


config=configparser.ConfigParser()
config.read("config.def")
output=config.get("OverAll", "output")
temp_dir=config.get("OverAll", "temp_dir")



class download:
    def __init__(self, output, temp_dir):
        self.output = output
        self.temp_dir = temp_dir
        os.chdir(self.temp_dir)


    def download_month(self, year, month):
      output = self.output+"{0}/".format(year)
      # 
      
      if not os.path.exists(output):
          os.makedirs(output)
          
      ndays = down.get_number_of_days(year,month)
      dmon = output+"3B-DAY.MS.MRG.3IMERG.{0}{1:02}-S000000-E235959.V06.nc".format(year, month)
      
      if not os.path.isfile(dmon):
        d = monthrange(year, month)[1]
        pool = multiprocessing.Pool(processes=4)
        L = down.get_DD_urls_day(year, month)
        nfile = len(glob.glob(self.temp_dir + "3B-DAY.MS.MRG.3IMERG.{0}{1:02}*".format(year,month)))
                
        while nfile<ndays:
            pool.map(down.download, L)
            nfile = len(glob.glob(self.temp_dir + "3B-DAY.MS.MRG.3IMERG.{0}{1:02}*".format(year,month)))
        pool.close()
        
        ds = xr.open_mfdataset(self.temp_dir + "3B-DAY.MS.MRG.3IMERG.{0}{1:02}*-S000000-E235959.V06.nc4".format(year,month))
        ds = ds["precipitationCal"]
        ds.to_netcdf(path=dmon, unlimited_dims = ["time"], engine = "netcdf4")
        del ds
        
        if os.path.isfile(dmon):
            subprocess.check_call(f"rm {self.temp_dir}"+ "/3B-DAY.MS.MRG.3IMERG.{0}*-S000000-E235959.V06.nc4".format(year), shell = True)
        else:
            print("error")
            sys.exit()
        

if __name__ == "__main__":
    d = download(output,temp_dir)
    for y in range(2001,2023):
        print("****", y, "****")
        for m in range(1,13):
            print("****", m, "/12 ****")
            d.download_month(y, m)

