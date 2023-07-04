#!/bin/bash
for y in {2008..2021}; do
  cd ${y}
  cdo cat 3B-DAY.MS.MRG.3IMERG.${y}* 3B-DAY.MS.MRG.3IMERG.${y}.V06.nc
  cd ..
done
