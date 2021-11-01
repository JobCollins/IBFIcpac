import pandas as pd
from utils import desinventar_processing, emdat_processing
import click
import urllib.request
import country_converter as coco
import zipfile
import os

@click.command()
@click.option('--country', default='kenya', help='country (e.g. kenya)')
@click.option('--disaster', default='flood', help='type of disaster (e.g. flood)')

def get_impact_data(country, disaster):
    print (country, ' ', disaster)

    # get country ISO
    iso3_code = coco.convert(names=[country], to='ISO3').lower()

    # initialize final impact data file 
    data = pd.read_csv('impact_data_template.csv', sep=';')

    # get DesInventar data
    base_url = 'https://www.desinventar.net/DesInventar/download/DI_export'
    try:
        urllib.request.urlretrieve('{}_{}.zip'.format(base_url, iso3_code), 'raw/DI_export_{}.zip'.format(iso3_code))
        with zipfile.ZipFile('raw/DI_export_{}.zip'.format(iso3_code), 'r') as zip_ref:
            zip_ref.extractall('raw')

        # convert to csv
        data_desinventar = desinventar_processing(input='raw/DI_export{}.xml'.format(iso3_code), output= 'raw/DI_processed_{}.csv'.format(iso3_code))

        # filter on disaster_type and add to final impact data
        data_desinventar = data_desinventar[data_desinventar['disaster_type'] == disaster]
        data = pd.concat([data, data_desinventar], sort=False, ignore_index=True)

        # remove Desinventar zipped data
        os.remove('raw/DI_export_{}.zip'.format(iso3_code))
    except:
        print('ERROR: DesInventar data not found, country not present or data wrongly formatted! Please check manually'
        'at https://www.desinventar.net')

    # get EM-DAT data
    if os.path.exists('raw/emdat_public.xlsx'):
        data_emdat = emdat_processing(input='raw/emdat_public.xlsx', output='raw/emdat_processed.csv', country_iso=iso3_code)

        # filter on disaster_type and add to final impact data
        print(data_emdat.head())
        data_emdat = data_emdat[data_emdat['disaster_type'] == disaster]
        data = pd.concat([data, data_emdat], sort=False, ignore_index=True)
    else:
        print('ERROR: EM-DAT data not found, please register at https://public.emdat.be/,'
              ' download and move to data_raw')

    # save
    data.to_csv('processed/{}_impact_data_v0.csv'.format(iso3_code))

if __name__ == '__main__':
    get_impact_data()

