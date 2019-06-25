#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 18:35:29 2018

@author: rishu
"""

import os
import tarfile
from extract_all import *

extract_data = "/home/rishu/vaari/Projects/1119/mas_lulc/data/Sat/extracted_2"

raw_data = "/home/rishu/vaari/Projects/1119/mas_lulc/data/Sat/raw_data_2/"

for roots, dirs, files in os.walk(raw_data):

    for fl in files:
        
        zip_file = os.path.join(roots, fl)
        
        extract_files(zip_file, extract_data)
        
        
        
        
# =============================================================================
#         zip_file = os.path.join(roots, fl)
#        
#         extract_files(zip_file, extracted_path)
# =============================================================================
       