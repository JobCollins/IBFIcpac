shp_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/tl_2019_16_prisecroads.shp'
csv_fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/roads.csv'
uri = 'file:///{}?delimiter={}'.format(csv_fn, ',')

csv = QgsVectorLayer(uri, 'roads.csv', 'delimitedtext')
shp = QgsVectorLayer(shp_fn, 'tl_2019_16_prisecroads', 'ogr')

ji = QgsVectorLayerJoinInfo()
ji.setJoinLayer(csv)
ji.setTargetFieldName('RTTYP')
ji.setJoinFieldName('RTTYP')
ji.setUsingMemoryCache(True)

shp.addJoin(ji)

QgsProject.instance().addMapLayer(shp)