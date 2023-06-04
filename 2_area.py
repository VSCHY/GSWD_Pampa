from shapely.geometry import Polygon
import numpy as np
import numpy.ma as ma
from src import *
import pandas as pd
import xarray as xr
import subprocess

#############################

reg = [[-62.070218922514414,-32.30474738845139],
       [-62.89537126401204,-32.30474738845139],
       [-62.89537126401204,-33.18217299905846],
       [-62.070218922514414,-33.18217299905846],
       [-62.070218922514414,-32.30474738845139]]
       
poly = Polygon(reg)

##########################
# Construct output with lon / lat

lon, lat, data = get_data_raster(1, 2010, poly)

xarlon = xr.IndexVariable("longitude", lon, 
        attrs={"units":"degrees_east",
               "standard_name": "longitude", 
               "long_name" : "longitude", 
               "axis":"X"})
xarlat = xr.IndexVariable("latitude", lat, 
        attrs={"units":"degrees_north",
               "standard_name": "latitude", 
               "long_name" : "latitude", 
               "axis":"Y"})
    
#################

dims = ['latitude',"longitude"]
coords = {'latitude':xarlat,"longitude":xarlon}

D_export = {}
D_export["data"] = xr.DataArray(data = data, dims = dims, coords = coords, attrs  = {"long_name":f"my data",'units': '-'}) 

ds = xr.Dataset(D_export,attrs = {})
ds.to_netcdf("sample_file.nc", encoding={'data': {'dtype': 'float'}})

subprocess.check_call("cdo gridarea sample_file.nc area_gswd_pampa.nc", shell = True)

#################
