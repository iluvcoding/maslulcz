#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 18:42:32 2018

@author: tomer
"""

from sentinelsat.sentinel import SentinelAPI
#import datetime as dt
import os

def download_s2(user, password, dir_raw, dir_nc, start_date, end_date, footprint, pr_status):


    api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus/')
    
    #footprint = "POLYGON((73 11, 74 11, 74 14, 73 14, 73 11))"
    products = api.query(footprint, date=(start_date, end_date), producttype='S2MSI1C')
   
    #print(products)
    
    for product in products:
        productInfo = api.get_product_odata(product)
        title = productInfo['title']
        tileNo_time = '%s_%s' % (title.split('_')[5], title.split('_')[2])
        try:
            downloadFlag = not pr_status[tileNo_time]
        except KeyError:
            pr_status[tileNo_time] = False
            downloadFlag =True
        #file_nc = os.path.join(dir_nc, "%s_VV.nc"%os.path.basename(title).split("_")[4])
        #file_nc = os.path.join(dir_nc, "%s_VV.nc" % title[17:48])
        file_wkt = os.path.join(os.path.dirname(dir_nc), "wkt/%s.wkt" % tileNo_time)
                
        if not os.path.exists(file_wkt):
            pFootPrint = productInfo['footprint']
            file = open(file_wkt, "a")
            file.write(pFootPrint)
            file.close()
        
        if downloadFlag:
            api.download(product, dir_raw, checksum=True)
        
    return pr_status