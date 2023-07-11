import xarray as xr
import pandas as pd
import numpy as np

def get_dire(year):
    dire = f"/media/anthony/easystore/PAMPA/IMERG_FINAL_Pampa/OUTPUT/{year}/3B-DAY.MS.MRG.3IMERG.{year}.V06.nc"
    return dire

minx=-62.89537126401204
maxx=-62.070218922514414
miny=-33.18217299905846
maxy=-32.30474738845139



for i, year in enumerate(np.arange(2001, 2022)):
    print(year)
    with xr.open_dataset(get_dire(year)) as ds:

        long_name = ds["precipitationCal"].long_name
        units = ds["precipitationCal"].units

        ds = ds.sel(lon=slice(-62.89537126401204,-62.070218922514414))
        ds = ds.sel(lat=slice(-33.18217299905846,-32.30474738845139))
        ds = ds.mean(dim = ["lat", "lon"])


        df = pd.DataFrame()
        df["date"] = pd.DatetimeIndex(ds.coords["time"].values)
        df["precipitationCal"] = ds["precipitationCal"].values
        df["unit"]= units
        df["Description"] = long_name
        df["Polygon (minx)"] = minx
        df["Polygon (maxx)"] = maxx
        df["Polygon (miny)"] = miny
        df["Polygon (maxy)"] = maxy
        if i == 0:
            df_out = df
        else:
            df_out = pd.concat([df_out, df])
df_out.to_excel("precipitationCal_IMERG_FINAL_2001_2021_Pampa.xlsx", index = False)
