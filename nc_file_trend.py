#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 12:08:28 2021

@author: Manish
"""

import xarray as xr
import numpy as np
import pymannkendall as mk 
import cartopy.crs as ccrs

import cartopy.io.shapereader as shpreader
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

observed = xr.open_dataset("/media/user/Other/IITB/CMIP6_Model_Evaluation/DATA/IMD/Indices/CDD_Index/CDD_IMD.nc")
observed = observed['consecutive_dry_days_index_per_time_period']
obs = observed.values

lats = observed.lat.values
lons = observed.lon.values

result = np.zeros([len(observed.lat.values),
                                           len(observed.lon.values)])
result[:] = np.nan
c=1
for i,lat in enumerate(lats):
    #print(c)
    #c+=1
    for j,lon in enumerate(lons):
        if (np.isnan(obs[0,i,j])):
            result[i,j] = np.nan
        else:
            y = obs[:,i,j]
            test=mk.original_test(y,alpha=0.05)
            result[i,j]=test.slope
            
ds = xr.Dataset({"trend": (('lat','lon'), result)},coords={'lat': lats, 'lon': lons,})
ds.trend.plot()


ds.to_netcdf("/media/user/ESD-ISO/sourabh/For_trend_manish/AGB_I_trend.nc") 


##plot
m = Basemap(projection='cyl',llcrnrlat=5,urcrnrlat=40,llcrnrlon=60,urcrnrlon=100.,lon_0=0.,resolution='i')
m.drawcoastlines(linewidth=0.5)
m.readshapefile("/home/user/Downloads/misc/IMD_GRIDDED_DATA/MAP/India_SHP/INDIA","India")
#m.drawcountries(linewidth=0.5)
m.drawparallels(np.arange(5,40,5.),linewidth=0.3)
m.drawmeridians(np.arange(60.,100.,5.),linewidth=0.3) 
ds.trend.plot()

plt.savefig("/home/user/Misc/navinya/t.png",dpi=300)
plt.show()
