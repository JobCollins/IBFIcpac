from qgis.PyQt import QtGui
import numpy as np

lyr = QgsProject.instance().mapLayersByName('USGS_NED_13_n45w116_IMG')[0]
stats = lyr.dataProvider().bandStatistics(1, QgsRasterBandStats.All)
min_val = stats.minimumValue
max_val = stats.maximumValue
color_ramp1 = ['#00ff80', '#005eff']
color_ramp2 = ['#ff0000', '#ffee00', '#002fff']

cr_symbol = QgsColorRampShader()
cr_symbol.setColorRampType(QgsColorRampShader.Interpolated)

# automatically define the color ramp list
breaks = np.linspace(min_val, max_val, len(color_ramp2))
ramp_list =[]
for i in range(len(breaks)):
    ramp_list.append(QgsColorRampShader.ColorRampItem(breaks[i], \
    QtGui.QColor(color_ramp2[i])))

# manually define the color ramp list
#ramp_list = [\
#QgsColorRampShader.ColorRampItem(min_val, QtGui.QColor(color_ramp1[0])), \
#QgsColorRampShader.ColorRampItem(max_val, QtGui.QColor(color_ramp1[1]))]

cr_symbol.setColorRampItemList(ramp_list)

cr_shader = QgsRasterShader()
cr_shader.setRasterShaderFunction(cr_symbol)
renderer = QgsSingleBandPseudoColorRenderer(lyr.dataProvider(), 1, cr_shader)
lyr.setRenderer(renderer)
lyr.triggerRepaint()