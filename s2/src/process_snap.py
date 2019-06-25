#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 19:55:12 2018

@author: thiyaku

Extract downloaded data and convert to L2A
"""
import glob
import os
import zipfile
from subprocess import call
def extract_download_data(zip_file, dir_tmp):
    
    file_name = os.path.join(dir_tmp, os.path.basename(zip_file[:-3]) + 'SAFE')

    if not os.path.exists(file_name):
        try:
            print("Extracting %s" % zip_file)
            zip_ref = zipfile.ZipFile(zip_file, 'r')
            zip_ref.extractall(dir_tmp)
            zip_ref.close()
        except:
            os.remove(zip_file)
            print('not downloaded properly')
    else:
        print("%s found, not extracting" % file_name)
    return file_name
    # break



def l1CTol2A(dir_raw, yyyymmdd,  dir_l1c, l2a_process_path, pr_status):
    zip_files = glob.glob(dir_raw + '/S2?_MSIL1C_%s*.zip' % yyyymmdd)
    for zip_file in zip_files:
        tileNo_time = '%s_%s' %(os.path.basename(zip_file).split('_')[5], os.path.basename(zip_file).split('_')[2])
        if not pr_status[tileNo_time]:
            safe_file = extract_download_data(zip_file, dir_l1c)
            cmd = '%s %s' % (l2a_process_path, safe_file)
            print(cmd)
            call(cmd, shell = True)
            #break