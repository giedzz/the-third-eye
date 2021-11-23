import pandas as pd
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

from utils.image_utils import create_rgb_image_from_bands
from utils.utils import unzip_file, delete_created_files

api = SentinelAPI('thethirdeye', 'thethirdeye123', 'https://scihub.copernicus.eu/dhus')

pg_out = pd.read_csv('pgAdminResults/limit_10000_test.csv')

# search by polygon, time, and SciHub query keywords
footprint = geojson_to_wkt(read_geojson('munich.geojson'))
products = api.query(footprint,
                     platformname='Sentinel-2',
                     cloudcoverpercentage=(0, 5))

for key, value in products.items():
    # download single scene by known product id
    # Try except implemented to exit only if we have downloaded image, if not print error and continue
    # Further steps would include unzipping downloaded image and creating images for classification training
    title = value['title']
    # title = 'S2A_MSIL2A_20211030T101141_N0301_R022_T32UQU_20211030T120510'
    try:
        print(value)
        api.download(key, 'data')
    except Exception as e:
        print(e)
        continue
    try:
        unzip_file(title)
    except Exception as e:
        print(e)
    img_path = create_rgb_image_from_bands(title, pg_out)
    delete_created_files(title)
    exit()
