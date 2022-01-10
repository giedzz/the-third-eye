import glob
import os

import numpy as np
import rasterio
import rasterio.warp
from osgeo import gdal
from rasterio.crs import CRS
from rasterio.mask import mask

from constants import DOWNLOAD_DIRECTORY, BUILDING_IMG_OUT, OUTPUT_BUILDING_PNG_PATH
from utils.utils import create_geo_json_from_polygon, get_features


def crop_building_from_tif(buildings_df, title, tif_img_pth):
    downloaded = False
    for key, row in buildings_df.iterrows():
        geo_json = create_geo_json_from_polygon(row['st_astext'])
        building_height = row['building_height']

        coords = get_features(geo_json)

        try:
            with rasterio.open(tif_img_pth) as src:
                coords = rasterio.warp.transform_geom(
                    CRS.from_epsg(4326),
                    CRS.from_epsg(str(src.crs).split(':')[1]),
                    coords
                )
                out_img, out_transform = mask(src, shapes=coords, crop=True, filled=False, pad=True, pad_width=5)

                out_meta = src.meta.copy()
            if is_sorta_black(out_img):
                continue
            out_meta.update({"driver": "GTiff", "height": out_img.shape[1], "width": out_img.shape[2],
                             "transform": out_transform})
            building_out_dir = os.path.join(BUILDING_IMG_OUT)
            os.makedirs(building_out_dir, exist_ok=True)
            building_out_img_path = os.path.join(building_out_dir, f'{title}-{key}-{building_height}.tiff')
            with rasterio.open(building_out_img_path, "w", **out_meta) as dest:
                dest.write(out_img)
            save_png_img(building_out_img_path)
            downloaded = True
        except ValueError:
            continue
    return downloaded


def save_png_img(input_geotiff_pth):
    os.makedirs(OUTPUT_BUILDING_PNG_PATH, exist_ok=True)
    output_png = os.path.join(OUTPUT_BUILDING_PNG_PATH, os.path.basename(input_geotiff_pth).replace('.tiff', '.jpg'))
    scale = '-scale min_val max_val'
    options_list = [
        '-ot Byte',
        '-of JPEG',
        scale
    ]
    options_string = " ".join(options_list)
    options_string = options_string.replace('\n', '')
    gdal.Translate(output_png,
                   input_geotiff_pth,
                   options=options_string)
    print('saved crop')


def get_tif_image_from_dir(title):
    extracted_image_data_path = os.path.join(DOWNLOAD_DIRECTORY, title, f'{title}.SAFE', 'GRANULE', '*', 'IMG_DATA',
                                             '*_TCI*')
    if not len(glob.glob(extracted_image_data_path)) > 0:
        extracted_image_data_path = os.path.join(DOWNLOAD_DIRECTORY, title, f'{title}.SAFE', 'GRANULE', '*', 'IMG_DATA',
                                                 'R10m', '*_TCI*')
    return glob.glob(extracted_image_data_path)[0]


def create_rgb_image_from_bands(title, buildings_df):
    try:
        tif_image_pth = get_tif_image_from_dir(title)
    except FileNotFoundError as e:
        print(e)
        try:
            tif_image_pth = get_tif_image_from_dir(title)
        except FileNotFoundError as e:
            print(e)
    return crop_building_from_tif(buildings_df, title, tif_image_pth)


def is_sorta_black(arr, threshold=0.9):
    tot = np.float(np.sum(arr))
    if tot/arr.size > (1-threshold):
        # print('is not black')
        return False
    else:
        # print('is kinda black')
        return True
