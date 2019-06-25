#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 18:16:09 2018

@author: tomer
"""

import glob
import os
#import numpy as np
import shutil
def processing_status(yyyymmdd, dir_nc):
    file_aots = glob.glob(os.path.join(dir_nc, "AOT/*%s*10m.nc"%yyyymmdd))
    status_dic = {}
    for file_aot in file_aots:
        tileno_time = os.path.basename(file_aot)[4:-11]
        file_ncs = glob.glob(os.path.join(dir_nc, "*/*%s*.nc" % tileno_time))
        ncFlag = len(file_ncs) == 35
        status_dic[tileno_time] = ncFlag
    return(status_dic)

def delete_file_fun(delete_files):
    delete_files = glob.glob(delete_files)
    for delete_file in delete_files:
        if os.path.exists(delete_file):
            try:
                os.remove(delete_file)
                print("%s deleted"%delete_file)
            except OSError:
                shutil.rmtree(delete_file)
                print("%s deleted"%delete_file)
            
            
def clean_dir(yyyymmdd, dir_tif, dir_l1c, dir_l2a, dir_raw, dir_nc):
    file_aots = glob.glob(os.path.join(dir_nc, "AOT/*%s*10m.nc"%yyyymmdd))
    for file_aot in file_aots:
        tileno_time = os.path.basename(file_aot)[:-11]
        file_ncs = glob.glob(os.path.join(dir_nc, "*/%s*.nc" % tileno_time))
        ncFlag = len(file_ncs) == 35
        if ncFlag:
            tileno = tileno_time.split('_')[1]
            time = tileno_time.split('_')[2]
            file_tifs = os.path.join(dir_tif, "*/%s*.tif" % tileno_time)
            # Delete only jp2 files
            file_l2a = os.path.join(dir_l2a, "*L2A_%s*%s*/GRANULE/*/IMG_DATA/*/*jp2" % (time, tileno))
            file_l1c = os.path.join(dir_l1c, "*L1C_%s*%s*" % (time, tileno))
            file_zip = os.path.join(dir_raw, "*L1C_%s*%s*" % (time, tileno))
            delete_file_fun(file_tifs)
            delete_file_fun(file_l2a)
            delete_file_fun(file_l1c)
            delete_file_fun(file_zip)