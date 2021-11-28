import pandas as pd
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

from utils.image_utils import create_rgb_image_from_bands
from utils.utils import unzip_file, sentinel_image_overlap_at_least_one_building, \
    read_already_downloaded_sentinel_data_titles, write_already_downloaded_sentinel_data_titles, delete_created_files

already_existing_files = read_already_downloaded_sentinel_data_titles('places.txt')

api = SentinelAPI('thethirdeye', 'thethirdeye123', 'https://scihub.copernicus.eu/dhus')

pg_out = pd.read_csv('pgAdminResults/munich_300.csv')

# search by polygon, time, and SciHub query keywords
footprint = geojson_to_wkt(read_geojson('munich.geojson'))
products = api.query(footprint,
                     platformname='Sentinel-2',
                     cloudcoverpercentage=(0, 5))

counter = 0
for key, value in products.items():
    if counter > 10:
        print('Downloaded >10 images now exiting...')
        exit()
    counter += 1
    # download single scene by known product id
    # Try except implemented to exit only if we have downloaded image, if not print error and continue
    # Further steps would include unzipping downloaded image and creating images for classification training
    title = value['title']
    DOWNLOAD = True
    UNZIP = True
    if title in already_existing_files:
        print('File already downloaded... Moving to next image...')
        continue
        # print('File already downloaded... Won\'t download...')
        # DOWNLOAD = False
        # UNZIP = False
    if not sentinel_image_overlap_at_least_one_building(pg_out, value['footprint']):
        print('Sentinel image does not overlap with any of the buildings, moving to next image...')
        continue
    # title = 'S2A_MSIL2A_20211010T100941_N0301_R022_T32UPU_20211010T115015'

    if DOWNLOAD:
        try:
            print(value)
            print('downloading...')
            api.download(key, 'data')
        except Exception as e:
            print(e)
            continue
    if UNZIP:
        try:
            unzip_file(title)
        except Exception as e:
            print(e)
    processed = create_rgb_image_from_bands(title, pg_out)
    # Delete files
    delete_created_files(title)
    # Append already processed files
    already_existing_files.append(title)
    write_already_downloaded_sentinel_data_titles('places.txt', already_existing_files)
    # if processed:
    #     exit()
