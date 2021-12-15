from osgeo import gdal, ogr
import os
import numpy as np
import csv
from PyQt5 import QtGui


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
    print(csv_fp)
    return shp_path, csv_fp

def table_join(shp_path, csv_fp, country):
    shp = QgsVectorLayer(shp_path, 'gadm36_{}_3_zstats'.format(country), 'ogr')
    shp.setDataSource(shp_path, 'gadm36_{}_3_zstats'.format(country), 'ogr')
    #QgsProject.instance().addMapLayer(shp)

    csv_path = 'file://{}?delimiter={}'.format(csv_fp, ',')
    csv = QgsVectorLayer(csv_path, '{}pop_zonal_stats'.format(country), 'delimitedtext')
    QgsProject.instance().addMapLayer(csv)

    shpField='zstats_id'
    csvField='id'

    joinObject = QgsVectorLayerJoinInfo()
    joinObject.setJoinLayer(csv)
    joinObject.setTargetFieldName(shpField)
    joinObject.setJoinFieldName(csvField)
    joinObject.setUsingMemoryCache(True)

    print("This: ", shp.addJoin(joinObject))

    
    myColumn = '{}pop_zonal_stats_count'.format(country)
    myRangeList = []
    myOpacity = 1

    ranges = []

    myMin1 = 0
    myMax1 = 40000
    myLabel1 = '0-40000'
    myColor1 = QtGui.QColor('#F5FBFF')
    ranges.append((myMin1, myMax1, myLabel1, myColor1))

    myMin2 = 41000
    myMax2 = 80000
    myLabel2 = '41000-80000'
    myColor2 = QtGui.QColor('#c7dcef')
    ranges.append((myMin2, myMax2, myLabel2, myColor2))

    myMin3 = 81000
    myMax3 = 120000
    myLabel3 = '81000-120000'
    myColor3 = QtGui.QColor('#72b2d7')
    ranges.append((myMin3, myMax3, myLabel3, myColor3))

    myMin4 = 121000
    myMax4 = 160000
    myLabel4 = '121000-160000'
    myColor4 = QtGui.QColor('#2878b8')
    ranges.append((myMin4, myMax4, myLabel4, myColor4))

    myMin5 = 161000
    myMax5 = 220000
    myLabel5 = '161000-220000'
    myColor5 = QtGui.QColor('#08306b')
    ranges.append((myMin5, myMax5, myLabel5, myColor5))

    for myMin, myMax, myLabel, myColor in ranges:
        mySymbol = QgsSymbol.defaultSymbol(shp.geometryType())
        mySymbol.setColor(myColor)
        mySymbol.setOpacity(myOpacity)
        myRange = QgsRendererRange(myMin, myMax, mySymbol, myLabel)
        myRangeList.append(myRange)

    myRenderer = QgsGraduatedSymbolRenderer('', myRangeList)
    myRenderer.setMode(QgsGraduatedSymbolRenderer.Quantile)
    myRenderer.setClassAttribute(myColumn)

    shp.setRenderer(myRenderer)

    QgsProject.instance().addMapLayer(shp)

def main():
    iso3_u = ['BDI', 'DJI', 'ETH', 'KEN', 'UGA', 'TZA', 'SSD', 'SOM', 'ERI', 'SDN', 'RWA']
    # iso3_l = [i.lower() for i in iso3_u]

    for i in iso3_u:
        data_fp = '/Users/jobdulo/Downloads/github/datasets/population/eappp/{}_ppp_2020.tiff'.format(i.lower())
        
        if i!= 'DJI' and i!='ERI' and i!='SOM':
            shp_fp = '/Users/jobdulo/Downloads/github/datasets/eadmin/gadm36_{}_shp/gadm36_{}_3.shp'.format(i, i)
            # print(i)
        else:
            # print('admin 2: ', i)
            shp_fp = '/Users/jobdulo/Downloads/github/datasets/eadmin/gadm36_{}_shp/gadm36_{}_2.shp'.format(i, i)

        zonal_statistics(shp_fp, data_fp)
        shp_path, csv_fp = write_zstats_csv(shp_fp, data_fp, 'population', i)
        table_join(shp_path, csv_fp, i)
#        graduate_layer(shp, i)

main()