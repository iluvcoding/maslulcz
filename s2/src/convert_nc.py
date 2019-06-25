#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 21:42:30 2018

@author: tomer
"""

from apya import raster
import numpy as np
from netCDF4 import Dataset, num2date, date2num
import datetime as dt
#import os
#import glob

def convert_nc(yyyymmdd, file_in, out_file):
    
    r = raster.ReadRaster(file_in)
    lons = np.linspace(r.xmin+0.5*r.xres, r.xmax-0.5*r.xres, r.ncol)
    lats = np.linspace(r.ymin+np.abs(0.5*r.yres), r.ymax-0.5*np.abs(r.xres), r.nrow)
    
    rootgrp = Dataset(out_file, "w", format="NETCDF4_CLASSIC")
    time = rootgrp.createDimension("time", None)
    lat = rootgrp.createDimension("lat", len(lats))
    lon = rootgrp.createDimension("lon", len(lons))
    
    times = rootgrp.createVariable("time","f8",("time",))
    latitudes = rootgrp.createVariable("lat","f8",("lat",))
    longitudes = rootgrp.createVariable("lon","f8",("lon",))
    var = rootgrp.createVariable("temp","f4",("time","lat","lon",), zlib=True, 
                                     least_significant_digit=1)
                                     
    data = np.flipud(r.data)
    
    #data[data>200] = np.nan
        
    latitudes[:] = lats
    longitudes[:] = lons
    var[0,:,] = data
        
    rootgrp.description = "Computed by Satyukt Analytics"
    rootgrp.history = "Created %s "%dt.date.today()
    rootgrp.source = "Estimated using vikleda"
    latitudes.units = "degrees north"
    longitudes.units = "degrees east"
    times.units = "days since 0001-01-01"
    times.calendar = "gregorian"
        
    dates = dt.datetime.strptime(yyyymmdd,'%Y%m%d')
    times[0] = date2num(dates, units=times.units, calendar=times.calendar)
    rootgrp.close()
    print('%s file created' % out_file)