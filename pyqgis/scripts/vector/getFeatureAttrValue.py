roads_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/tl_2019_16_prisecroads.shp'
states_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_us_state/tl_2019_us_state.shp'

roads_lyr = QgsVectorLayer(roads_fn, 'roads', 'ogr')

print(roads_fn)
print(states_fn)

print(roads_lyr)

for field in roads_lyr.fields():
    print(field.name())
    
roads_fc = roads_lyr.featureCount()

for fid in range(10, 20):
    feat = roads_lyr.getFeature(fid)
    print(feat['FULLNAME'])