fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_place/id_cities.shp'
lyr = QgsVectorLayer(fn, 'cities', 'ogr')

#CALCULATE DISTANCE BETWEEN TWO CITIES IN DEGREES
feat0 = lyr.getFeature(0)
print(feat0['NAME'])
feat1 = lyr.getFeature(1)
print(feat1['NAME'])

geom0 = feat0.geometry()
geom1 = feat1.geometry()

dist01 = geom0.distance(geom1)

print('The distance between', feat0['NAME'], 'and', feat1['NAME'], \
'is', dist01, 'degrees')