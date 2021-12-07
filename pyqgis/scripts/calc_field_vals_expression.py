fn = '/Users/jobdulo/Downloads/github/datasets/lines.shp'
lyr = QgsVectorLayer(fn, 'lines', 'ogr')

pv = lyr.dataProvider()

pv.addAttributes([QgsField('length', QVariant.Double),\
QgsField('divide', QVariant.Double),\
QgsField('x', QVariant.Double),\
QgsField('y', QVariant.Double)])
lyr.updateFields()

expl = QgsExpression('$length')
expd = QgsExpression('"length"/"Value"')
expx = QgsExpression('$x')
expy = QgsExpression('$y')

context = QgsExpressionContext()
context.appendScopes(\
QgsExpressionContextUtils.globalProjectLayerScopes(lyr))

with edit(lyr):
    for feat in lyr.getFeatures():
        context.setFeature(feat)
        feat['length'] = expl.evaluate(context)
        feat['x'] = expx.evaluate(context)
        feat['y'] = expy.evaluate(context)
        lyr.updateFeature(feat)

with edit(lyr):
    for feat in lyr.getFeatures():
        context.setFeature(feat)
        feat['divide'] = expd.evaluate(context)
        lyr.updateFeature(feat)

QgsProject.instance().addMapLayer(lyr)