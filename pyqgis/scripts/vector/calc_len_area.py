fn_states = '/Users/jobdulo/Downloads/github/datasets/tl_2019_us_state/tl_2019_us_state.shp'
fn_roads = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/tl_2019_16_prisecroads.shp'

lyr_states = QgsVectorLayer(fn_states, 'states', 'ogr')
lyr_roads = QgsVectorLayer(fn_roads, 'roads', 'ogr')

# CALCULATE STATE AREA IN SQ DEGREES
state_feats = lyr_states.getFeatures()
for sfeat in state_feats:
    geom = sfeat.geometry()
    sarea = geom.area()
    print(sfeat['NAME'], ':', sarea, 'square degrees')

# CALCULATE ROAD LENGTH IN DEGREES  
road_feats = lyr_roads.getFeatures()
for rfeat in road_feats:
    geom = rfeat.geometry()
    rlen = geom.length()
    print(rfeat['FULLNAME'], ':', rlen, 'degrees')