#SAVE MULTIPLE LAYERS
out_fn = '/Users/jobdulo/Downloads/github/IBFIcpac/pyqgis/scripts/maps/id_cities_roads.png'
lyr_cities = QgsProject.instance().mapLayersByName('id_cities')[0]
lyr_roads = QgsProject.instance().mapLayersByName('tl_2019_16_prisecroads')[0]

img = QImage(QSize(800, 800), QImage.Format_ARGB32_Premultiplied)

color = QColor(255, 255, 255, 255)
img.fill(color.rgba())

p = QPainter()
p.begin(img)
p.setRenderHint(QPainter.Antialiasing)

ms = QgsMapSettings()
ms.setBackgroundColor(color)
ms.setLayers([lyr_roads, lyr_cities])
rect = QgsRectangle(ms.fullExtent())
rect.scale(1.1)
ms.setExtent(rect)
ms.setOutputSize(img.size())

render = QgsMapRendererCustomPainterJob(ms, p)
render.start()
render.waitForFinished()
p.end()

# save the image
img.save(out_fn)