# JOIN BY LOCATION
cities_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_place/id_cities.shp'
roads_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/tl_2019_16_prisecroads.shp'
place_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_place/tl_2019_16_place.shp'
loc_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_place/joinbyloc_citiesplaces.shp'

processing.run('qgis:joinattributesbylocation', \
{'INPUT': cities_fn, \
'JOIN': place_fn, \
'PREDICATE': 0, \
'METHOD': 0, \
'OUTPUT': loc_fn})

iface.addVectorLayer(loc_fn, '', 'ogr')

# JOIN BY NEAREST
# check closest road to a city
near_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_place/joinbynear_citiesroads.shp'

processing.run('qgis:joinbynearest', \
{'INPUT': cities_fn, \
'INPUT_2': roads_fn, \
'OUTPUT': near_fn})

iface.addVectorLayer(near_fn, '', 'ogr')