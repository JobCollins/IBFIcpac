fn = '/Users/jobdulo/Downloads/github/datasets/lines.shp'
lyr = QgsVectorLayer(fn, 'lines', 'ogr')

pv = lyr.dataProvider()

# CREATE NEW FIELD BASED ON CALCULATION
pv.addAttributes([QgsField('calc1', QVariant.Double)])
lyr.updateFields()

lyr.startEditing()
for feat in lyr.getFeatures():
    print('start value', feat['calc1'])
    feat['calc1'] = feat['Value'] * feat['Value']
    print('end value', feat['calc1'])
    lyr.updateFeature(feat)
lyr.commitChanges()

iface.addVectorLayer(fn, '', 'ogr')