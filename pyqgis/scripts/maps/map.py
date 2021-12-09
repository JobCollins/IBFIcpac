lyr_cities = QgsProject.instance().mapLayersByName('id_cities')[0]
lyr_roads = QgsProject.instance().mapLayersByName('tl_2019_16_prisecroads')[0]

# save an instance of the project
proj = QgsProject.instance()
mgr = proj.layoutManager()
layout_name = 'Layout1'

# delete any layout with same name as layout_name
for lyt in mgr.layouts():
    if lyt.name() == layout_name:
      mgr.removeLayout(lyt)

# create a print layout
lyt = QgsPrintLayout(proj)
lyt.initializeDefaults()
lyt.setName(layout_name)
mgr.addLayout(lyt)

# setup the map
map = QgsLayoutItemMap(lyt)
map.setRect(20, 20, 20, 20)

# map settings
ms = QgsMapSettings()
ms.setLayers([lyr_cities, lyr_roads])
rect = QgsRectangle(ms.fullExtent())
rect.scale(1.1)
ms.setExtent(rect)
map.setExtent(rect)
map.setBackgroundColor(QColor(255, 255, 255))
lyt.addLayoutItem(map)

# move map to a new location in the layout
map.attemptMove(QgsLayoutPoint(5, 20, QgsUnitTypes.LayoutMillimeters))
map.attemptResize(QgsLayoutSize(180, 180, QgsUnitTypes.LayoutMillimeters))

# add legend
leg = QgsLayoutItemLegend(lyt)
leg.setTitle('Legend')
layerTree = QgsLayerTree()
layerTree.addLayer(lyr_cities)
layerTree.addLayer(lyr_roads)
leg.model().setRootGroup(layerTree)
lyt.addLayoutItem(leg)
leg.attemptMove(QgsLayoutPoint(230, 20, QgsUnitTypes.LayoutMillimeters))

# add title
tlt = QgsLayoutItemLabel(lyt)
tlt.setText('Idaho Cities and Roads')
tlt.setFont(QFont('Arial', 24))
tlt.adjustSizeToText()
lyt.addLayoutItem(tlt)
tlt.attemptMove(QgsLayoutPoint(5, 5, QgsUnitTypes.LayoutMillimeters))

# add scale bar
sb = QgsLayoutItemScaleBar(lyt)
sb.setStyle('Line Ticks Up')
sb.setUnits(QgsUnitTypes.DistanceKilometers)
sb.setNumberOfSegments(4)
sb.setNumberOfSegmentsLeft(0)
sb.setUnitsPerSegment(50)
sb.setUnitLabel('km')
sb.setFont(QFont('Arial', 14))
sb.setLinkedMap(map)
lyt.addLayoutItem(sb)
sb.attemptMove(QgsLayoutPoint(200, 150, QgsUnitTypes.LayoutMillimeters))

lyt = mgr.layoutByName(layout_name)
exporter = QgsLayoutExporter(lyt)

fn = '/Users/jobdulo/Downloads/github/IBFIcpac/pyqgis/scripts/maps/map.pdf'
exporter.exportToPdf(fn, QgsLayoutExporter.PdfExportSettings())