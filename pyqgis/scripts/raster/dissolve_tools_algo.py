# DISSOLVE
from qgis import processing

input_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/tl_2019_16_prisecroads.shp'
output_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/roads_all.shp'
output_fn2 = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/roads_type.shp'

# take a vector layer and combine their features
# into new features based on attribute(s)
processing.run('native:dissolve', \
{'INPUT': input_fn,\
'OUTPUT': output_fn})

processing.run('native:dissolve', \
{'INPUT': input_fn,\
'FIELD': ['RTTYP'],\
'OUTPUT': output_fn2})

iface.addVectorLayer(output_fn2, '', 'ogr')