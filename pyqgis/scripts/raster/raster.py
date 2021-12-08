# OPEN RASTER LAYER
fn = '/Users/jobdulo/Downloads/github/datasets/USGS_NED_13_n45w116_IMG/USGS_NED_13_n45w116_IMG.img'

# load layer and add to interface
# lyr = iface.addRasterLayer(fn)

# load layer without adding to interface
lyr = QgsRasterLayer(fn)

print('height', lyr.height())
print('width', lyr.width())
print('bands', lyr.bandCount())

# RASTER STATISTICS
stats = lyr.dataProvider().bandStatistics(1, QgsRasterBandStats.All)

print('min', stats.minimumValue)
print('mean', stats.mean)
print('max', stats.maximumValue)
print('range', stats.range)
print('sum', stats.sum)
print('std dev', stats.stdDev)
print('sum squares', stats.sumOfSquares)

# IDENTIFY RASTER VALUES AT A LOCATION
lyr_name = "USGS_NED_13_n45w116_IMG"
lyr = QgsProject.instance().mapLayersByName(lyr_name)[0]

val, res = lyr.dataProvider().sample(QgsPointXY(-115.715, 44.893), 1)
print(val)

ident = lyr.dataProvider().identify(QgsPointXY(-115.715, 44.893), \
QgsRaster.IdentifyFormatValue)

print(ident.isValid())
print(ident.results())