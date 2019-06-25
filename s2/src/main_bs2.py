#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 18:32:06 2018

@author: tomer
"""

import os
import getpass
import datetime as dt

from download_s2 import download_s2
from process_snap import l1CTol2A
from change_resolution import change_resolution
#from process_snap import process_snap
#from change_resolution import change_resolution
#from convert_nc import convert_nc

from clean_dir import clean_dir
from clean_dir import processing_status
import numpy as np
############ System specific inputs #######################
username = getpass.getuser()
if username == "satyukt":
    dir_vaari = "/media/edrive2/vaari/Projects/1000/bindusen/s2/"
    path_gpt = "/home/satyukt/Tools/snap/bin/gpt"
    path_s2c = "/home/satyukt/Tools/sen2cor/Sen2Cor-02.05.05-Linux64/bin" # Path to Sen2Cor

    

################ Generic inputs ############################
res = {'10m':0.0001, '20m':0.0002, '60m':0.0006} # in degree

user = 'sktomer'
password = '804480'

dir_raw = os.path.join(dir_vaari, "raw_data")
#dir_tmp = os.path.join(dir_vaari, 'tmp')
dir_tif = os.path.join(dir_vaari, "tif")
dir_nc = os.path.join(dir_vaari, "nc")
dir_l1c = os.path.join(dir_vaari, 'l1c')
dir_l2a = os.path.join(dir_vaari, 'l2a')

#dir_l2a = os.path.join(dir_vaari, 'ndvi')
dir_src = os.path.dirname(os.path.realpath(__file__))
#file_xml = os.path.join(dir_src, 'IW_GRDH_1SDV_orig1.xml')
l2a_process_path = os.path.join(path_s2c, 'L2A_Process')
dir_project = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

## Here you are passingh the file. Instead Change this to footprint as in main_bs1.py

file_area = os.path.join(dir_project, "area", "ka_s2.csv")
file = open(file_area, "r")
footprint = file.read()
file.close()
###### main #############################
start_date = dt.date(2017,10,1)
end_date = dt.date.today()
ndays = (end_date - start_date).days + 1

for td in range(ndays):
    cur_dt = start_date + dt.timedelta(days=td)
    dt1 = cur_dt + dt.timedelta(days=1)
    yyyymmdd = "%s%02d%02d"%(cur_dt.year, cur_dt.month, cur_dt.day)
    yyyymmdd1 = "%s%02d%02d"%(dt1.year, dt1.month, dt1.day)
    pr_status = processing_status(yyyymmdd, dir_nc)
    pr_status = download_s2(user, password, dir_raw, dir_nc, yyyymmdd, yyyymmdd1, footprint, pr_status)
    if not np.array(list(pr_status.values())).all():
    
        # Convert L1C to L2A
        l1CTol2A(dir_raw, yyyymmdd,  dir_l1c, l2a_process_path, pr_status)
        change_resolution(yyyymmdd, dir_l2a, dir_tif, dir_nc, res)
    
    
    #mosaic_ndvi(dir_tmp, dir_tif, yyyymmdd)
    #tif_to_nc(dir_nc, dir_tif, yyyymmdd, res)
    #change_resolution(yyyymmdd, dir_dim, dir_tif, res)
    #convert_nc(yyyymmdd, dir_tif, dir_nc)
    clean_dir(yyyymmdd, dir_tif, dir_l1c, dir_l2a, dir_raw, dir_nc)
    print(yyyymmdd)
    #break
