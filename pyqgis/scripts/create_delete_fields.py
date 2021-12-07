# CREATE AND ADD FIELDS
fn = '/Users/jobdulo/Downloads/github/datasets/lines.shp'
lyr = QgsVectorLayer(fn, 'lines', 'ogr')

pv = lyr.dataProvider()

pv.addAttributes([QgsField('new_field1', QVariant.String), \
QgsField('new_field2', QVariant.Double)])

iface.addVectorLayer(fn, '', 'ogr')

# DELETE FIELDS
fn = '/Users/jobdulo/Downloads/github/datasets/lines.shp'
lyr = QgsVectorLayer(fn, 'lines', 'ogr')

pv = lyr.dataProvider()

pv.deleteAttributes([3, 4])

iface.addVectorLayer(fn, '', 'ogr')
