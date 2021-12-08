from qgis.PyQt import QtGui

lyr = QgsProject.instance().mapLayersByName('id_cities')[0]
field_name = 'ALAND'
breaks = [39033, 100000, 1000000, 216713666]
colors_list = ['#e0a6ff', '#c354ff', '#a600ff']
rangeList = []

for i in range(len(breaks)-1):
    min_val = breaks[i]
    max_val = breaks[i+1]
    symbol = QgsSymbol.defaultSymbol(lyr.geometryType())
    symbol.setColor(QtGui.QColor(colors_list[i]))
    range_label = str(breaks[i]) + '-' + str(breaks[i+1])
    rangeList.append(QgsRendererRange(min_val, max_val, symbol, range_label))

renderer = QgsGraduatedSymbolRenderer(field_name, rangeList)
lyr.setRenderer(renderer)
lyr.triggerRepaint()