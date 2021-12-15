from .raster_offsets import boundingBoxToOffsets, geotFromOffsets, setFeatureStats
from osgeo import gdal, ogr
import os
import numpy as np
import csv

def zonal_statistics(shp_fp, data_fp):
    mem_driver = ogr.GetDriverByName("Memory")
    mem_driver_gdal = gdal.GetDriverByName("MEM")
    shp_name = "temp"

    pop_ds = gdal.Open(data_fp)
    adm_ds = ogr.Open(shp_fp, 1)

    lyr = adm_ds.GetLayer()
    lyr_defn = lyr.GetLayerDefn()


    geot = pop_ds.GetGeoTransform()
    # print(geot)
    nodata = pop_ds.GetRasterBand(1).GetNoDataValue()



    zstats = []
    fids = []
    adm_feat = lyr.GetNextFeature()
    niter = 0



    while adm_feat:
        if adm_feat.GetGeometryRef() is not None:
            if os.path.exists(shp_name):
                mem_driver.DeleteDataSource(shp_name)
            tadm_ds = mem_driver.CreateDataSource(shp_name)
            tadm_lyr = tadm_ds.CreateLayer('admin', None, ogr.wkbPolygon)
            tadm_lyr.CreateFeature(adm_feat.Clone())
            offsets = boundingBoxToOffsets(adm_feat.GetGeometryRef().GetEnvelope(),geot)
    #        print(offsets)
            new_geot = geotFromOffsets(offsets[0], offsets[2], geot)
            
            tpop_ds = mem_driver_gdal.Create("",\
            offsets[3] - offsets[2],\
            offsets[1] - offsets[0],\
            1,\
            gdal.GDT_Byte)
            
            tpop_ds.SetGeoTransform(new_geot)
            gdal.RasterizeLayer(tpop_ds, [1], tadm_lyr, burn_values=[1])
            tpop_array = tpop_ds.ReadAsArray()
            
            pop_array = pop_ds.GetRasterBand(1).ReadAsArray(\
            offsets[2], \
            offsets[0], \
            offsets[3] - offsets[2], \
            offsets[1] - offsets[0])
            
            id = adm_feat.GetFID()
    #        adm_feat.SetField('zstats_id', id)
    #        lyr.SetFeature(adm_feat)
            
            if pop_array is not None:
                maskarray = np.ma.MaskedArray(\
                pop_array,\
                mask = np.logical_or(pop_array==nodata, np.logical_not(tpop_array)))
                
                if maskarray is not None:
                    zstats.append(setFeatureStats(\
                    id,\
                    maskarray.min(),\
                    maskarray.max(),\
                    maskarray.mean(),\
                    np.ma.median(maskarray),\
                    maskarray.std(),\
                    maskarray.sum(),\
                    maskarray.count()
                    ))
                else:
                    zstats.append(setFeatureStats(\
                    id,\
                    nodata,\
                    nodata,\
                    nodata,\
                    nodata,\
                    nodata,\
                    nodata,\
                    nodata
                    ))
            else:
                zstats.append(setFeatureStats(\
                    id,\
                    nodata,\
                    nodata,\
                    nodata,\
                    nodata,\
                    nodata,\
                    nodata,\
                    nodata
                    ))
            
            tadm_ds = None
            tadm_lyr = None
            tpop_ds = None
                
            
            adm_feat = lyr.GetNextFeature()
    return zstats, adm_ds, lyr
