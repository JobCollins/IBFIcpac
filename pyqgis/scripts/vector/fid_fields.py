fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/tl_2019_16_prisecroads.shp'
lyr = QgsVectorLayer(fn, 'roads', 'ogr')

# CREATE FID
pv = lyr.dataProvider()

pv.addAttributes([QgsField('fid', QVariant.Int)])
lyr.updateFields()

lyr.startEditing()
for feat in lyr.getFeatures():
    feat['fid'] = feat.id()
    lyr.updateFeature(feat)

lyr.commitChanges()

# SELECT FID
lyr = iface.addVectorLayer(fn, '', 'ogr')

select_ids = [0, 3, 5, 6, 7, 8]

lyr.select(select_ids)

# GET INFO OF SELECTED FEATURES
print('selected count', lyr.selectedFeatureCount())
print('selected fids', lyr.selectedFeatureIds())

lyr_selection = lyr.selectedFeatures()

for feat in lyr_selection:
    print(feat['fid'], feat['FULLNAME'])