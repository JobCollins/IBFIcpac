states_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_us_state/tl_2019_us_state.shp'
fn = '/Users/jobdulo/Downloads/github/datasets/points.shp'
fn_line = '/Users/jobdulo/Downloads/github/datasets/lines.shp'
fn_polygon = '/Users/jobdulo/Downloads/github/datasets/plygons.shp'

# create fields
lyr_fields = QgsFields()
lyr_fields.append(QgsField('ID', QVariant.Int))
lyr_fields.append(QgsField('Name', QVariant.String))
lyr_fields.append(QgsField('Value', QVariant.Double))

# CREATE A POINT LAYER
# write vector file to disk and give crs
writer = QgsVectorFileWriter(fn, 'UTF-8', lyr_fields, QgsWkbTypes.Point,\
QgsCoordinateReferenceSystem('EPSG:4326'), 'ESRI Shapefile')

feat = QgsFeature()
geom = QgsGeometry.fromPointXY(QgsPointXY(-109.00, 40.0))
feat.setGeometry(geom)
feat.setAttributes([1, 'First feature', 2.3])
writer.addFeature(feat)

iface.addVectorLayer(fn, '', 'ogr')

del(writer)

# CREATE A LINE LAYER
# write vector file to disk and give crs
writer = QgsVectorFileWriter(fn_line, 'UTF-8', lyr_fields, QgsWkbTypes.LineString,\
QgsCoordinateReferenceSystem('EPSG:4326'), 'ESRI Shapefile')

feat = QgsFeature()
geom =  QgsGeometry.fromPolyline([QgsPoint(-117.0, 47.0), QgsPoint(-112.0, 39.0),\
QgsPoint(-100.0, 40.0)])
feat.setGeometry(geom)
feat.setAttributes([1, 'First feature', 2.3])
writer.addFeature(feat)

iface.addVectorLayer(fn_line, '', 'ogr')

del(writer)


# CREATE A POLYGON LAYER
# write vector file to disk and give crs
writer = QgsVectorFileWriter(fn_polygon, 'UTF-8', lyr_fields, QgsWkbTypes.Polygon,\
QgsCoordinateReferenceSystem('EPSG:4326'), 'ESRI Shapefile')

feat = QgsFeature()

for i in range(0,5):
    geom = QgsGeometry.fromPolygonXY([[\
    QgsPointXY(-117.0 + i, 47.0 - i), \
    QgsPointXY(-112.0 + i*1.5, 39.0 - i*1.5),\
    QgsPointXY(-100.0 + i*2, 40.0 - i*2)]])
    feat.setGeometry(geom)
    feat.setAttributes([i, str(i) + ' feature', i**i])
    writer.addFeature(feat)
    
iface.addVectorLayer(fn_polygon, '', 'ogr')

del(writer)

