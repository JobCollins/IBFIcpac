from modularized.zonal_stats_csv import write_zstats_csv
from modularized.zonal_stats import zonal_statistics
from modularized.table_join import table_join, graduate_layer

def main():
    iso3_u = ['BDI', 'DJI', 'ETH', 'KEN', 'UGA', 'TZA', 'SSD', 'SOM', 'ERI', 'SDN', 'RWA']
    # iso3_l = [i.lower() for i in iso3_u]

    for i in iso3_u:
        data_fp = '/Users/jobdulo/Downloads/github/datasets/population/eappp/{}_ppp_2020.tiff'.format(i.lower())
        
        if i!= 'DJI' and i!='ERI' and i!='SOM':
            shp_fp = '/Users/jobdulo/Downloads/github/datasets/eadmin/gadm36_{}_shp/gadm36_{}_3.shp'.format(i, i)
            # print(i)
        else:
            # print('admin 2: ', i)
            shp_fp = '/Users/jobdulo/Downloads/github/datasets/eadmin/gadm36_{}_shp/gadm36_{}_2.shp'.format(i, i)

        zonal_statistics(shp_fp, data_fp)
        shp_path, csv_fp = write_zstats_csv(shp_fp, data_fp, 'population', i)
        shp = table_join(shp_path, csv_fp)
        graduate_layer(shp)

if __name__ == '__main__':
   main()