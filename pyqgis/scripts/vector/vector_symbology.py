#BASIC POINT(MARKER) SYMBOLS
lyr = QgsProject.instance().mapLayersByName('id_cities')[0]

pt_symbol = QgsMarkerSymbol.createSimple({'name': 'diamond', \
'color': '#00bbff'})
lyr.renderer().setSymbol(pt_symbol)
lyr.triggerRepaint()

# BASIC LINE AND POLYGON SYMBOLS
# edit line layer symbology
line_lyr = QgsProject.instance().mapLayersByName('id_roads_usi')[0]
line_symbol = QgsLineSymbol.createSimple({'line_style': 'dash', \
'color': 'red', 'line_width': '0.86'})
line_lyr.renderer().setSymbol(line_symbol)
line_lyr.triggerRepaint()

# print the symbology dictionary for any layer.
print(line_lyr.renderer().symbol().symbolLayers()[0].properties())


#edit polygon layer symbology
poly_lyr = QgsProject.instance().mapLayersByName('tl_2019_16_place')[0]
poly_symbol = QgsFillSymbol.createSimple({'color': 'green',\
'outline_color': 'red', 'outline_style': 'dash', 'outline_width': '1.0'})
poly_lyr.renderer().setSymbol(poly_symbol)
poly_lyr.triggerRepaint()