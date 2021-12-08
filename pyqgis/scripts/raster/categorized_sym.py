from qgis.PyQt import QtGui
import numpy as np

lyr = QgsProject.instance().mapLayersByName('USGS_NED_13_n45w116_IMG')[0]
stats = lyr.dataProvider().bandStatistics(1, QgsRasterBandStats.All)
min_val = stats.minimumValue
max_val = stats.maximumValue
color_ramp = ['#ff0000', '#ffee00', '#002fff']

cr_symbol = QgsColorRampShader()
cr_symbol.setColorRampType(QgsColorRampShader.Discrete)

breaks = [1600, 2300, 4000]

ramp_list =[]
for i in range(len(breaks)):
    if i == 0:
        low_val = str(min_val)
    else:
        low_val = str(breaks[i-1])
    high_val = str(breaks[i])
    ramp_list.append(QgsColorRampShader.ColorRampItem(breaks[i], \
    QtGui.QColor(color_ramp2[i]), low_val + '-' + high_val))
cr_symbol.setColorRampItemList(ramp_list)

cr_shader = QgsRasterShader()
cr_shader.setRasterShaderFunction(cr_symbol)
renderer = QgsSingleBandPseudoColorRenderer(lyr.dataProvider(), 1, cr_shader)
lyr.setRenderer(renderer)
lyr.triggerRepaint()