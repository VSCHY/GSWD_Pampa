import xarray as xr
import pandas as pd
import numpy as np

def get_dire(year):
    dire = f"/media/anthony/easystore/PAMPA/IMERG_FINAL_Pampa/OUTPUT/{year}/3B-DAY.MS.MRG.3IMERG.{year}.V06.nc"
    return dire

minx=-73
maxx=-50
miny=-54
maxy=-20


-73,-50,-54,-20
for i, year in enumerate(np.arange(2001, 2022)):
    print(year)
    with xr.open_dataset(get_dire(year)) as ds:

        long_name = ds["precipitationCal"].long_name
        units = ds["precipitationCal"].units

        ds = ds.sel(lon=slice(minx,maxx))
        ds = ds.sel(lat=slice(miny,maxy))
        ds.to_netcdf(f"Argentina/3B-DAY.MS.MRG.3IMERG.{year}.V06_ARG.nc", engine = "netcdf4")
