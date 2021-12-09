# SAVE A LAYER AS AN IMAGE
out_fn = '/Users/jobdulo/Downloads/github/IBFIcpac/pyqgis/scripts/maps/id_cities.png'
lyr = QgsProject.instance().mapLayersByName('id_cities')[0]

# setup image to write to
img = QImage(QSize(800, 800), QImage.Format_ARGB32_Premultiplied)

# setup bg of image to solid white
color = QColor(255, 255, 255, 255)
img.fill(color.rgba())

# setup painter
p = QPainter()
p.begin(img)
p.setRenderHint(QPainter.Antialiasing) # smooth out any rectangular shapes

# setup the map
ms = QgsMapSettings()
ms.setBackgroundColor(color)
ms.setLayers([lyr])
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