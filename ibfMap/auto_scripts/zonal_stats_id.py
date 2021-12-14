from osgeo import gdal, ogr
import os
import numpy as np
import csv


shp_fn = '/Users/jobdulo/Downloads/github/datasets/eadmin/gadm36_KEN_shp/gadm36_KEN_3.shp'
population = '/Users/jobdulo/Downloads/github/datasets/population/eappp/ken_ppp_2020.tiff'

pop_ds = gdal.Open(population)
adm_ds = ogr.Open(shp_fn, 1)

lyr = adm_ds.GetLayer()
lyr_defn = lyr.GetLayerDefn()

driver = ogr.GetDriverByName("ESRI Shapefile")
outds = driver.CreateDataSource("/Users/jobdulo/Downloads/github/datasets/eadmin/gadm36_KEN_shp/gadm36_KEN_3_zstats.shp")
outlayer = adm_ds.CopyLayer(lyr, 'gadm36_KEN_3_zstats')

# create the new id field to match up with zstats ids        
new_field = ogr.FieldDefn('zstats_id', ogr.OFTInteger)
outlayer.CreateField(new_field)

for feat in outlayer:
    feat.SetField('zstats_id', feat.GetFID())
    outlayer.SetFeature(feat)
    
outlayer = outds = None