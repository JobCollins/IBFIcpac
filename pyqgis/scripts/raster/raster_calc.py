dem_fn = '/Users/jobdulo/Downloads/github/datasets/USGS_NED_13_n45w116_IMG/USGS_NED_13_n45w116_IMG.img'
dem_lyr = QgsRasterLayer(dem_fn)

out_fn = '/Users/jobdulo/Downloads/github/datasets/USGS_NED_13_n45w116_IMG/rascalc_result.tif'

entries = []

dem = QgsRasterCalculatorEntry()
dem.ref = 'dem@1'
dem.raster = dem_lyr
dem.bandNumber = 1
entries.append(dem)

# add 1 to the dem
ras_calc1 = QgsRasterCalculator('dem@1 + 1.0', out_fn, 'GTiff', \
dem_lyr.extent(), dem_lyr.width(), dem_lyr.height(), entries)

ras_calc1.processCalculation()

iface.addRasterLayer(dem_fn)
iface.addRasterLayer(out_fn)