from shapely.geometry import Polygon
import numpy as np
import numpy.ma as ma
from src import *
import pandas as pd
import xarray as xr
from netCDF4 import Dataset
import datetime
from tqdm import tqdm

#############################
"""
reg = [[-62.070218922514414,-32.30474738845139],
       [-62.89537126401204,-32.30474738845139],
       [-62.89537126401204,-33.18217299905846],
       [-62.070218922514414,-33.18217299905846],
       [-62.070218922514414,-32.30474738845139]]
"""

reg = [[-62.070218922514414,-32.30474738845139],    
    [-62.89537126401204,-32.30474738845139],   
    [-62.89537126401204,-33.18217299905846],
    [-62.070218922514414,-33.18217299905846],
    [-62.070218922514414,-32.30474738845139]]
       
poly = Polygon(reg)

##########################

nc = Dataset("area_gswd_pampa.nc", "r")
lons = nc.variables["longitude"][:]
lats = nc.variables["latitude"][:]
area = nc.variables["cell_area"][:]

##########################
tsize = np.sum([1 for year in range(2000,2022) for month in range(1,13)])

out_array = np.zeros((tsize, len(lats), len(lons)), dtype = np.float32)

dates = []

i = 0
for year in tqdm(range(2000,2022)):
    for month in range(1,13):
        #D = {}        
        #_, _, data = get_data_raster(month, year, poly)
        #out = ma.masked_where(data==255, data)/100
        #out_array[i,:,:] = out
        dates.append(datetime.date(year,month,1))
        i +=1
        
##########################

D_export = {}
time = pd.DatetimeIndex(dates)
xarlon = xr.IndexVariable("longitude", lons, attrs={"unit":"degrees_east","standard_name": "longitude", "long_name" : "longitude", "axis":"X"})
xarlat = xr.IndexVariable("latitude", lats, attrs={"unit":"degrees_north","standard_name": "latitude", "long_name" : "latitude", "axis":"Y"})

dims = ['time', 'latitude',"longitude"]
coords = {"time":time, 'latitude':xarlat, "longitude":xarlon}


D_export["GSWD_floodfrac"] = xr.DataArray(
    data = out_array, 
    dims = dims, 
    coords = coords, 
    attrs  = {"long_name":f"Flood fraction from GSWD",'units': "Flooded Fraction"})
   
D_export["cell_area"] = xr.DataArray(
    data = area, 
    dims = ['latitude',"longitude"], 
    coords = {'latitude':xarlat, "longitude":xarlon}, 
    attrs  = {"long_name":f"cell_area",'units': "m2"})

ds = xr.Dataset(D_export,attrs = {})
ds.to_netcdf("Output_Flooded_frac.nc")
ds.close()
##########################

##########################

#Open the file as netCDf and fill progressively

i = 0
with Dataset("Output_Flooded_frac.nc", "r+") as nc:
  for year in tqdm(range(2000,2022)):
    for month in range(1,13):
        _, _, data = get_data_raster(month, year, poly)
        data = data.astype(np.float32)
        #data[data==255.] = -999.
        data = ma.masked_where(data==255, data)
        nc.variables["GSWD_floodfrac"][i,:,:] = data
        nc.sync()
        i += 1

