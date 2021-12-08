# CENTROID OF POLYGON
# points at the center of each polygon in data
fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_place/tl_2019_16_place.shp'
fn_out = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_place/id_cities.shp'

lyr = QgsVectorLayer(fn, '', 'ogr')

writer = QgsVectorFileWriter(fn_out, 'UTF-8', lyr.fields(), QgsWkbTypes.Point,\
lyr.sourceCrs(), 'ESRI Shapefile')

feats = lyr.getFeatures()

for feat in feats:
    poly_geom = feat.geometry()
    point_geom = poly_geom.centroid()
    feat.setGeometry(point_geom)
    writer.addFeature(feat)

del(writer)