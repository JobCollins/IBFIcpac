from osgeo import gdal, ogr
import os
import numpy as np
import csv

def boundingBoxToOffsets(bbox, geot):
    col1 = int((bbox[0] - geot[0])/geot[1])
    col2 = int((bbox[1] - geot[0])/geot[1]) + 1
    row1 = int((bbox[3] - geot[3])/geot[5])
    row2 = int((bbox[2] - geot[3])/geot[5]) + 1
    return [row1, row2, col1, col2]

def geotFromOffsets(row_offset, col_offset, geot):
    new_geot = [
        geot[0] + (col_offset * geot[1]),
        geot[1],
        0.0,
        geot[3] + (row_offset * geot[5]),
        0.0,
        geot[5]
    ]
    return new_geot
    
def setFeatureStats(fid, min, max, mean, median, sd, sum, count, names = ["min", "max", "mean", "median", "sd", "sum", "count", "id"]):
    featstats = {
        names[0]: min,
        names[1]: max,
        names[2]: mean,
        names[3]: median,
        names[4]: sd,
        names[5]: sum,
        names[6]: count,
        names[7]:fid
    }
    return featstats

shp_fn = '/Users/jobdulo/Downloads/github/datasets/eadmin/gadm36_KEN_shp/gadm36_KEN_3.shp'
population = '/Users/jobdulo/Downloads/github/datasets/population/eappp/ken_ppp_2020.tiff'

mem_driver = ogr.GetDriverByName("Memory")
mem_driver_gdal = gdal.GetDriverByName("MEM")
shp_name = "temp"

pop_ds = gdal.Open(population)
adm_ds = ogr.Open(shp_fn, 1)

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
        tadm_lyr = tadm_ds.CreateLayer('admin3', None, ogr.wkbPolygon)
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
        
## create the new id field to match up with zstats ids        
#pv = lyr.dataProvider()
#pv.addAttributes([QgsField('zstats_id', QVariant.Int]))
#lyr.updateFields()
#
#lyr.startEditing()
        
#lyr.commitChanges()

csv_fn = '/Users/jobdulo/Downloads/github/IBFIcpac/ibfMap/auto_scripts/data/zstats.csv'
col_names = zstats[0].keys()
with open(csv_fn, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, col_names)
    writer.writeheader()
    writer.writerows(zstats)

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


print("Done!")

# Add layers to interface
    









