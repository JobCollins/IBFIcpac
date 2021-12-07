# CREATE A BUFFER AROUND ROADS
fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/tl_2019_16_prisecroads.shp'
fn_out = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/id_roads_buffer.shp'

lyr = QgsVectorLayer(fn, '', 'ogr')

writer = QgsVectorFileWriter(fn_out, 'UTF-8', lyr.fields(),\
QgsWkbTypes.Polygon,\
lyr.sourceCrs(), 'ESRI Shapefile')

feats = lyr.getFeatures()

for feat in feats:
    line_geom = feat.geometry()
    buf_geom = line_geom.buffer(0.1, 5)
    feat.setGeometry(buf_geom)
    writer.addFeature(feat)

del(writer)