library(raster)
library(rgdal)
library(sp)

# Area of interest /home/rishu/vaari/Projects/1119/mas_lulc/data/Sat/AOI

in.folders = Sys.glob("/home/rishu/vaari/Projects/1119/mas_lulc/data/Sat/extracted_2/*")

mainDir = "/home/rishu/vaari/Projects/1119/mas_lulc"

kml.bnds = readOGR("/home/rishu/Projects/1119/mas_lulc/kml/enlarged_Chennai.kml", pointDropZ = T)

s.f = "/home/rishu/vaari/Projects/1119/mas_lulc/data/Sat/extracted/LC081420502018010701T1-SC20181220044002/LC08_L1TP_142050_20180107_20180119_01_T1_pixel_qa.tif"

nkml.bnds = spTransform(x = kml.bnds, crs(raster(s.f)))

ext.kml =  extent(nkml.bnds)

intersect.fold <- c()

i = 1
#checking the folders with overlapping extents
for(folder in in.folders)
{
  path = paste(folder, "*", sep = "/")
  
  in.files = Sys.glob(path)
  
  qa.ras = raster(in.files[3])
  
  c = intersect(extent(qa.ras), ext.kml)
  
  if(typeof(c) == 'NULL'){
    
    print("bekaar")
  
    }
  else{
    
    intersect.fold <- c(intersect.fold, folder)
    
    print(folder)
  
    }
  
}

intersect.fold


for(folder in intersect.fold)
{
  folder_name = unlist(strsplit(unlist(strsplit(folder, "/"))[11], "-"))[1]
  
  landsat = substr(folder_name, 1, 4)
  
  folder_name = unlist(strsplit(folder_name, "-"))[1]
  
  folder_name = paste(substr(folder_name, 1, 4), substr(folder_name, 10, 18), sep ="")
  
  
  
  if(landsat == "LC08")
  {
  
    path = paste(folder, "*.tif", sep = "/")
    
    in.files = Sys.glob(path)
    
    p.qa = raster(in.files[1])
    
    p.crop = crop(p.qa, ext.kml)
    
    p.vals = raster::getValues(p.crop)
    
    # 2800, 2804, 2808, 2812, 6896, 6900, 6904, 6908
    p.vals[p.vals == 2800] = -999
    p.vals[p.vals == 2804] = -999
    p.vals[p.vals == 2808] = -999
    p.vals[p.vals == 2812] = -999
    p.vals[p.vals == 6896] = -999
    p.vals[p.vals == 6900] = -999
    p.vals[p.vals == 6904] = -999
    p.vals[p.vals == 6908] = -999
    
    
    for(i in (1:10))
    {
      file = in.files[i]
      
      ras = raster(file)
      
      new.ras = crop(ras, ext.kml)
      
      ras.val = raster::getValues(new.ras)
      
      ras.val[p.vals == -999] = -999
      
      dir.create(file.path(mainDir, "data", "Sat", "AOI", folder_name), recursive = TRUE, showWarnings = F)
      
      f_n = unlist(strsplit(basename(file), "_"))
      
      f = paste(f_n[1], f_n[4], f_n[9], sep = "_")
      
      file_name = paste("/home/rishu/vaari/Projects/1119/mas_lulc/data/Sat/AOI", folder_name, f, sep = "/")
      
      print(file_name)
      
      raster::setValues(new.ras, ras.val)
      
      #raster::writeRaster(new.ras, filename = file_name, overwrite = T)
      
    }
  }
    else if(landsat == "LE07" || landsat == "LT05")
    {
      path = paste(folder, "*.tif", sep = "/")
      
      in.files = Sys.glob(path)
      
      p.qa = raster(in.files[1])
      
      p.crop = crop(p.qa, ext.kml)
      
      p.vals = raster::getValues(p.crop)
      
      # 752, 756, 760, 764
      p.vals[p.vals == 752] = -999
      p.vals[p.vals == 756] = -999
      p.vals[p.vals == 760] = -999
      p.vals[p.vals == 764] = -999
      
      for(i in (1:10))
      {
        file = in.files[i]
        
        ras = raster(file)
        
        new.ras = crop(ras, ext.kml)
        
        ras.val = raster::getValues(new.ras)
        
        ras.val[p.vals == -999] = -999
        
        dir.create(file.path(mainDir, "data", "Sat", "AOI", folder_name), recursive = TRUE, showWarnings = F)
        
        f_n = unlist(strsplit(basename(file), "_"))
        
        f = paste(f_n[1], f_n[4], f_n[9], sep = "_")
        
        file_name = paste("/home/rishu/vaari/Projects/1119/mas_lulc/data/Sat/AOI", folder_name, f, sep = "/")
        
        print(file_name)
        
        raster::setValues(new.ras, ras.val)
        
        #raster::writeRaster(new.ras, filename = file_name, overwrite = T)
        
      }
    }
  
}
