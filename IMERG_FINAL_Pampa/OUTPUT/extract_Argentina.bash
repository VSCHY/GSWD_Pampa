#!/bin/bash

mkdir Argentina
year=2001
cdo sellonlatbox,-73,-50,-54,-20 ${year}/3B-DAY.MS.MRG.3IMERG.${year}.V06.nc Argentina/3B-DAY.MS.MRG.3IMERG.${year}.V06_ARG.nc
