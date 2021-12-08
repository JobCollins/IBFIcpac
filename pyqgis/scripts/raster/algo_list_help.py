for alg in QgsApplication.processingRegistry().algorithms():
        print(alg.id(), "->", alg.displayName())
processing.algorithmHelp("qgis:buffer")