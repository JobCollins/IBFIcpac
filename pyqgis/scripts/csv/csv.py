# LOAD CSV FILE

fn = '/Users/jobdulo/Downloads/github/datasets/tl_2019_16_prisecroads/roads.csv'
uri = 'file:///{}?delimiter={}'.format(fn, ',')
iface.addVectorLayer(uri, '', 'delimitedtext')