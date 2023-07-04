import rioxarray
import rasterio
from shapely.ops import transform
import glob
from rasterio.merge import merge
from rasterio.mask import mask
from pyproj import transform as tr
from functools import partial
import pyproj
from shapely.geometry import Polygon
import numpy as np
import numpy.ma as ma


def get_data_raster(month, year, poly):
    """
    Get the data in a raster over a specific polygon
    """
    # 
    filename_in = f'./Originals/{year}_{month:02d}_percent.tif'
    filename_out = "./TEMP/temp.tif"

    try:
        with rasterio.open(filename_in) as src0:
            out_image, out_transform = mask(dataset=src0, shapes=[poly], crop=True)
            out_meta = src0.meta.copy()
        out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})
        with rasterio.open(filename_out, "w", **out_meta) as dest:
            dest.write(out_image)
    except:
        print("An error has occurred, maybe there is no data over the Polygon")
        print("Take care that the Polygon and raster have the same projection")

     
    with rioxarray.open_rasterio(filename_out) as rds:
        lon = rds.x
        lat = rds.y
        data = rds.data[0,:,:]
    return lon, lat, data
