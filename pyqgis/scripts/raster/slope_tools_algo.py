#SLOPE
from qgis import processing

input_fn = '/Users/jobdulo/Downloads/github/datasets/USGS_NED_13_n45w116_IMG/USGS_NED_13_n45w116_IMG.img'
output_qgis = '/Users/jobdulo/Downloads/github/datasets/USGS_NED_13_n45w116_IMG/slope_qgis.tif'
output_gdal = '/Users/jobdulo/Downloads/github/datasets/USGS_NED_13_n45w116_IMG/slope_gdal.tif'

# calculates the angle of inclination of terrain
# from a raster layer
processing.run('qgis:slope',
{'INPUT': input_fn, \
'Z_FACTOR': 1.0, \
'OUTPUT': output_qgis})

processing.run('gdal:slope',
{'INPUT': input_fn, \
'BAND': 1, \
'OUTPUT': output_gdal})

iface.addRasterLayer(output_gdal)