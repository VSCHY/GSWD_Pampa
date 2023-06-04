# GSWD_Pampa
Extraction of the Global surface water dynamics (1999-2021) dataset. Mapsin 10x10°tiles. Here extraction of the data for the Pampa region.

From [GLAD WEBSITE](https://glad.umd.edu/dataset/global-surface-water-dynamics)


Individual Month Maps values:
- between 0 and 100, monthly mean water percent
- 255 no data

## Installation

```bash
conda create -n GSWD_Pampa -c conda-forge rasterio rioxarray shapely pyproj webdriver-manager selenium netcdf4
conda activate GSWD_Pampa
```


## Download

```python
conda activate
python download.py
```

## Extraction
```python
python extract.py
```
