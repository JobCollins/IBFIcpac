# CATEGORIZED SYMBOLOGY
# with road types
from random import randrange

lyr = QgsProject.instance().mapLayersByName('tl_2019_16_prisecroads')[0]
field_idx = lyr.fields().indexFromName('RTTYP')
field_vals = lyr.uniqueValues(field_idx)

cats = []
for val in field_vals:
    symbol = QgsSymbol.defaultSymbol(lyr.geometryType())
    cat_style = {}
    cat_style['line_color'] = str(randrange(0, 256)) + ',' + \
    str(randrange(0, 256)) + ',' + str(randrange(0, 256)) + ',' + str(255)
    cat_symbol = QgsSimpleLineSymbolLayer.create(cat_style)
    symbol.changeSymbolLayer(0, cat_symbol)
    cat = QgsRendererCategory(val, symbol, val)
    cats.append(cat)

renderer = QgsCategorizedSymbolRenderer('RTTYP', cats)
lyr.setRenderer(renderer)
lyr.triggerRepaint()