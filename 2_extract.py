from shapely.geometry import Polygon
import numpy as np
import numpy.ma as ma
from src import *
import pandas as pd

#############################

reg = [[-62.070218922514414,-32.30474738845139],
       [-62.89537126401204,-32.30474738845139],
       [-62.89537126401204,-33.18217299905846],
       [-62.070218922514414,-33.18217299905846],
       [-62.070218922514414,-32.30474738845139]]
       
poly = Polygon(reg)

##########################

L = []
for year in range(2000,2022):
    for month in range(1,13):
        D = {}        
        lon, lat, data = get_data_raster(month, year)
        nsize = data.size
        missing = np.count_nonzero(data == 255)/nsize
        out = ma.masked_where(data==255, data)/100
        flooded = np.sum(out)/nsize
        D = {"Date":f"01/{month:02d}/{year}","missing":missing, "flooded":flooded}
        L.append(D)
        
df = pd.DataFrame.from_dict(L, orient = "columns")



