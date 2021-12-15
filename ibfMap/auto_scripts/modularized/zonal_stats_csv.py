from .zonal_stats import zonal_statistics
from osgeo import gdal, ogr
import os
import numpy as np
import csv

def write_zstats_csv(shp_fp, data_fp, data_name, country):
    csv_fp = '/Users/jobdulo/Downloads/github/IBFIcpac/ibfMap/auto_scripts/data/{}_{}_zstats.csv'.format(country, data_name)
    zstats, adm_ds, lyr = zonal_statistics(shp_fp, data_fp)
    col_names = zstats[0].keys()
    with open(csv_fp, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, col_names)
        writer.writeheader()
        writer.writerows(zstats)

    driver = ogr.GetDriverByName("ESRI Shapefile")
    shp_path = "/Users/jobdulo/Downloads/github/datasets/eadmin/gadm36_{}_shp/gadm36_{}_3_zstats.shp".format(country, country)
    outds = driver.CreateDataSource(shp_path)
    outlayer = adm_ds.CopyLayer(lyr, 'gadm36_{}_3_zstats'.format(country))

    # create the new id field to match up with zstats ids        
    new_field = ogr.FieldDefn('zstats_id', ogr.OFTInteger)
    outlayer.CreateField(new_field)

    for feat in outlayer:
        feat.SetField('zstats_id', feat.GetFID())
        outlayer.SetFeature(feat)
        
    outlayer = outds = None


    print("Done writing zonal stats to csv!")
    return shp_path, csv_fp