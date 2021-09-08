#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 14:27:06 2021

@author: user
"""
import xarray as xr
import numpy as np
import pymannkendall as mk 

observed = xr.open_rasterio("/media/user/ESD-ISO/sourabh/For_trend_manish/AGB_I_Files/AGB_I_2000.tif")
obs = observed.values

lats = observed.x.values
lons = observed.y.values

stack = np.zeros([19,len(observed.y.values),len(observed.x.values)])
stack[:] = np.nan

l = np.genfromtxt("/media/user/ESD-ISO/sourabh/For_trend_manish/AGB_I_Files/AGB_I.txt",dtype=str) ##list of tiff file
for i in range(0,19):
    observed = xr.open_rasterio("/media/user/ESD-ISO/sourabh/For_trend_manish/AGB_I_Files/"+l[i])
    obs = observed.values
    stack[i::]= obs

result = np.zeros([len(observed.y.values),len(observed.x.values)])
result[:] = np.nan
c=1
for i,lat in enumerate(lats):
    print(c)
    c+=1
    for j,lon in enumerate(lons):
        if (np.isnan(stack[0,j,i])):
            result[j,i] = np.nan
        else:
            y = stack[:,j,i]
            test=mk.original_test(y,alpha=0.05)
            result[j,i]=test.slope
            
ds = xr.Dataset({"trend": (('lat','lon'), result)},coords={'lon': observed.x.values, 'lat': observed.y.values,})
ds.to_netcdf("/media/user/ESD-ISO/sourabh/For_trend_manish/AGB_I_trend.nc") 
ds.trend.plot()