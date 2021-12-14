

shp_path = '/Users/jobdulo/Downloads/github/datasets/eadmin/gadm36_KEN_shp/gadm36_KEN_3_zstats.shp'
shp = QgsVectorLayer(shp_path, 'gadm36_KEN_3_zstats', 'ogr')
shp.setDataSource(shp_path, 'gadm36_KEN_3_zstats', 'ogr')
#QgsProject.instance().addMapLayer(shp)

csv_path = 'file:///Users/jobdulo/Downloads/github/IBFIcpac/ibfMap/auto_scripts/data/zstats.csv?delimiter={}'.format(',')
csv = QgsVectorLayer(csv_path, 'kepop_zonal_stats', 'delimitedtext')
#QgsProject.instance().addMapLayer(csv)

shpField='zstats_id'
csvField='id'

joinObject = QgsVectorLayerJoinInfo()
joinObject.setJoinLayer(csv)
joinObject.setTargetFieldName(shpField)
joinObject.setJoinFieldName(csvField)
joinObject.setUsingMemoryCache(True)

print("This: ", shp.addJoin(joinObject))

from PyQt5 import QtGui

myColumn = 'kepop_zonal_stats_count '
myRangeList = []
myOpacity = 1

ranges = []

myMin1 = 0
myMax1 = 40000
myLabel1 = '0-40000'
myColor1 = QtGui.QColor('#F5FBFF')
ranges.append((myMin1, myMax1, myLabel1, myColor1))

myMin2 = 41000
myMax2 = 80000
myLabel2 = '41000-80000'
myColor2 = QtGui.QColor('#c7dcef')
ranges.append((myMin2, myMax2, myLabel2, myColor2))

myMin3 = 81000
myMax3 = 120000
myLabel3 = '81000-120000'
myColor3 = QtGui.QColor('#72b2d7')
ranges.append((myMin3, myMax3, myLabel3, myColor3))

myMin4 = 121000
myMax4 = 160000
myLabel4 = '121000-160000'
myColor4 = QtGui.QColor('#2878b8')
ranges.append((myMin4, myMax4, myLabel4, myColor4))

myMin5 = 161000
myMax5 = 220000
myLabel5 = '161000-220000'
myColor5 = QtGui.QColor('#08306b')
ranges.append((myMin5, myMax5, myLabel5, myColor5))

for myMin, myMax, myLabel, myColor in ranges:
  mySymbol = QgsSymbol.defaultSymbol(shp.geometryType())
  mySymbol.setColor(myColor)
  mySymbol.setOpacity(myOpacity)
  myRange = QgsRendererRange(myMin, myMax, mySymbol, myLabel)
  myRangeList.append(myRange)

myRenderer = QgsGraduatedSymbolRenderer('', myRangeList)
myRenderer.setMode(QgsGraduatedSymbolRenderer.Quantile)
myRenderer.setClassAttribute(myColumn)

shp.setRenderer(myRenderer)

QgsProject.instance().addMapLayer(shp)


