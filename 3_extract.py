from shapely.geometry import Polygon
import numpy as np
import numpy.ma as ma
from src import *
import pandas as pd
import xarray as xr
from netCDF4 import Dataset

#############################

reg = [[-62.070218922514414,-32.30474738845139],
       [-62.89537126401204,-32.30474738845139],
       [-62.89537126401204,-33.18217299905846],
       [-62.070218922514414,-33.18217299905846],
       [-62.070218922514414,-32.30474738845139]]
       
poly = Polygon(reg)

##########################

nc = Dataset("area_gswd_pampa.nc", "r")
area = nc.variables["cell_area"][:]
total_area = np.sum(area)

##########################

L = []
for year in range(2000,2022):
    for month in range(1,13):
        D = {}        
        lon, lat, data = get_data_raster(month, year, poly)
        
        missing = ma.masked_where(data!=255, data)
        missing[missing == 255] = 1
        missing_area = np.sum(missing*area)
        missing_frac = missing_area/total_area
        
        out = ma.masked_where(data==255, data)/100
        flooded_area = np.sum(out*area)
        flooded_frac = flooded_area//total_area
        
        D = {"Date":f"01/{month:02d}/{year}",
             "missing_area (m2)":missing_area, 
             "missing_frac (-)":missing_frac,
             "flooded_area (m2)":flooded_area,
             "flooded_frac (-)":flooded_frac}
             
        L.append(D)
        
df = pd.DataFrame.from_dict(L, orient = "columns")
df.to_excel("Output_GSWD.xlsx")
##########################

