#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 20:16:00 2018

@author: tomer
"""

import glob
import os
from subprocess import call
from convert_nc import convert_nc

def translateRaster(in_ras, out_ras, res, proj='EPSG:4326'):
    SC = "gdalwarp %s %s -t_srs %s -tr %f %f -tap"%(in_ras, out_ras, proj, res, res)
    call(SC, shell=True)

def change_resolution(yyyymmdd, dir_l2a, dir_tif,dir_nc, res):
    
    #basename = os.path.basename(file_zip)
    #out_file = os.path.join(dim_dir, basename[:32] + '.dim')
        
    dirs_in = glob.glob(os.path.join(dir_l2a, "S2?_MSIL2A_%s*/GRANULE/*"%yyyymmdd))
    
    for dir_in in dirs_in:
        
        
        jp2_files = glob.glob(os.path.join(dir_in,  'IMG_DATA/*/*jp2'))
        for jp2_file in jp2_files:
            jp2_basename = os.path.basename(jp2_file)[:-4]
            band = jp2_basename.split('_')[3]
            
            res_deg = res[jp2_basename.split('_')[4]]
            nc_file = os.path.join(dir_nc,band, "%s.nc" % jp2_basename)
            if not os.path.exists(nc_file):
                if not os.path.exists(os.path.dirname(nc_file)):
                        os.makedirs(os.path.dirname(nc_file))
                tif_file = os.path.join(dir_tif,band, "%s.tif" % jp2_basename)
                if not os.path.exists(tif_file):
                    if not os.path.exists(os.path.dirname(tif_file)):
                        os.makedirs(os.path.dirname(tif_file))
                    translateRaster(jp2_file, tif_file, res_deg)
                convert_nc(yyyymmdd, tif_file, nc_file)