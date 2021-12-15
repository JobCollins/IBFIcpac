

def boundingBoxToOffsets(bbox, geot):
    col1 = int((bbox[0] - geot[0])/geot[1])
    col2 = int((bbox[1] - geot[0])/geot[1]) + 1
    row1 = int((bbox[3] - geot[3])/geot[5])
    row2 = int((bbox[2] - geot[3])/geot[5]) + 1
    return [row1, row2, col1, col2]

def geotFromOffsets(row_offset, col_offset, geot):
    new_geot = [
        geot[0] + (col_offset * geot[1]),
        geot[1],
        0.0,
        geot[3] + (row_offset * geot[5]),
        0.0,
        geot[5]
    ]
    return new_geot
    
def setFeatureStats(fid, min, max, mean, median, sd, sum, count, names = ["min", "max", "mean", "median", "sd", "sum", "count", "id"]):
    featstats = {
        names[0]: min,
        names[1]: max,
        names[2]: mean,
        names[3]: median,
        names[4]: sd,
        names[5]: sum,
        names[6]: count,
        names[7]:fid
    }
    return featstats

