# CLIP VECTOR LAYERS
from qgis import processing

input_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/tl_2019_16_prisecroads.shp'
overlay_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_place/tl_2019_16_place.shp'
output_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_place/roads_places_clip.shp'

# extract the road layers that overlay place boundaries layers
processing.run("native:clip", \
{'INPUT': input_fn,\
'OVERLAY': overlay_fn,\
'OUTPUT': output_fn})

iface.addVectorLayer(output_fn, '', 'ogr')