roads_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/copy_tl_2019_16_prisecroads.shp'
states_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_us_state/tl_2019_us_state.shp'

roads_lyr = QgsVectorLayer(roads_fn, 'roads', 'ogr')

print(roads_fn)
print(states_fn)

print(roads_lyr)

# Get layer fields
for field in roads_lyr.fields():
    print(field.name())
    
# Get feature attribute values
roads_fc = roads_lyr.featureCount()

for fid in range(10, 20):
    feat = roads_lyr.getFeature(fid)
    print(feat['FULLNAME'])
    
# also to get features...
# feats = roads_lyr.getFeatures()
# for feat in feats:
#    print(feat['FULLNAME'])

# Copying a Layer
# QgsVectorFileWriter.writeAsVectorFormat(roads_lyr, '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/copy_tl_2019_16_prisecroads.shp', 'utf-8', driverName='ESRI Shapefile')
    
# Get feature geometry
feats = roads_lyr.getFeatures()
feat0 = roads_lyr.getFeature(0)
# for feat in feats:
#     geom = feat.geometry()

# Change value of an attribute
lyr_fields = roads_lyr.fields()
ftc = lyr_fields.indexFromName('FULLNAME')
feat0.setAttribute(ftc, 'Change the road name')
roads_lyr.startEditing()
roads_lyr.updateFeature(feat0)
roads_lyr.commitChanges()

# Change All Attribute Values
attrs = ['1002', 'Changed ALL features', 'MyType2', 'New2']
roads_lyr.startEditing()
feat0.setAttributes(attrs)
roads_lyr.updateFeature(feat0)
roads_lyr.commitChanges()
# change all features attrs
for feat in feats:
    roads_lyr.startEditing()
    feat.setAttributes(attrs)
    roads_lyr.updateFeature(feat)
    roads_lyr.commitChanges()

# Change a feature's geometry
feat0_geom = feat0.geometry()
point1 = QgsPoint(-117.0, 43.59915)
point2 = QgsPoint(-110.0, 43.59915)
newgeom = QgsGeometry.fromPolyline([point1, point2])
# newgeommulti = QgsGeometry.fromMultiPolylineXY([point1, point2])
roads_lyr.startEditing()
feat0.setGeometry(newgeom)
roads_lyr.updateFeature(feat0)
roads_lyr.commitChanges()

# Create a new feature and add to a layer
newfeat = QgsFeature(roads_lyr.fields())
newfeat.setAttributes(['1005', 'Added a new one', 'ZZ', 'ZZ'])
geom = QgsGeometry.fromPolyline([QgsPoint(-117.0, 40.0), \
QgsPoint(-110.0, 40,0)])
newfeat.setGeometry(geom)
roads_lyr.dataProvider().addFeatures([newfeat])


