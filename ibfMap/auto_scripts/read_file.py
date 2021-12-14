def get_vector_lyr(filepath):
    data_vector_lyr = QgsVectorLayer(filepath, '', 'ogr')
    print('File path: ', file_path)
    
    return data_vector_lyr
    
def get_lyr_fields(filepath):
    vector_lyr = get_vector_lyr(filepath)
    for field in vector_lyr.fields():
        print(field.name())
        
#def create_copy_lyr(filepath):
#    QgsVectorFileWriter.writeAsVectorFormat(get_vector_lyr(filepath), '/Users/jobdulo/Downloads/github/IBFIcpac/ibfMap/auto_scripts/data/copy{}'.format(, 'utf-8', driverName='ESRI Shapefile')

