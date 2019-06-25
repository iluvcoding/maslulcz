#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 18:35:40 2018

@author: rishu
"""
import tarfile

from subprocess import call

import os

def extract_files(input_zip, extracted_path):
    
    print input_zip
    
    path = extracted_path + "/" + input_zip.split("/")[10].split(".")[0]
   
    os.mkdir(path)
    
    cmd = "tar -xvf " + input_zip + " -C " + path 
    
    call(cmd, shell=True)
    
    
# =============================================================================
#     tar = tarfile.open(input_zip, "r.gz")
#     
#     tar.extractall(path)
#     
#     tar.close()
#     
# =============================================================================
    
    
# =============================================================================
#     try:
#         
#         os.mkdir(path)
#     except:
#         print "donot worry"
#     
#     tar = tarfile.open(input_zip, "r:gz")  
#         
#     tar.extractall(path)
#     
#     tar.close()
# =============================================================================
