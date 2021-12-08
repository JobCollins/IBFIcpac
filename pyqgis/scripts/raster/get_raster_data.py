# GET DATA FOR ALL THE GRIDS IN THE RASTER
from osgeo import gdal

lyr_name = "USGS_NED_13_n45w116_IMG"
lyr = QgsProject.instance().mapLayersByName(lyr_name)[0]
fn = lyr.dataProvider().dataSourceUri()

ds = gdal.Open(fn)
data = ds.GetRasterBand(1).ReadAsArray()
print("data shape: ",data.shape)
print(data[0,0], data[10812, 10812], data[5400, 5400])