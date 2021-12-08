dem_fn = '/Users/jobdulo/Downloads/github/datasets/USGS_NED_13_n45w116_IMG/USGS_NED_13_n45w116_IMG.img'
dem_lyr = QgsRasterLayer(dem_fn)
dem1_lyr = QgsRasterLayer('/Users/jobdulo/Downloads/github/datasets/USGS_NED_13_n45w116_IMG/rascalc_result.tif')

out_fn = '/Users/jobdulo/Downloads/github/datasets/USGS_NED_13_n45w116_IMG/rascalc_result_divide.tif'

entries = []

dem = QgsRasterCalculatorEntry()
dem.ref = 'dem@1'
dem.raster = dem_lyr
dem.bandNumber = 1
entries.append(dem)

dem1 = QgsRasterCalculatorEntry()
dem1.ref = 'dem1@1'
dem1.raster = dem1_lyr
dem1.bandNumber = 1
entries.append(dem1)

ras_calc = QgsRasterCalculator('dem1@1 / dem@1 * 100.0', out_fn, 'GTiff',\
dem_lyr.extent(), dem_lyr.width(), dem_lyr.height(), entries)
ras_calc.processCalculation()

iface.addRasterLayer(dem_fn)
iface.addRasterLayer(out_fn)