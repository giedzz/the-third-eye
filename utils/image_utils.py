import glob
import os

import rasterio
import rasterio.warp
from rasterio.crs import CRS
from rasterio.mask import mask

from constants import DOWNLOAD_DIRECTORY, TIF_IMAGE_DIRECTORY, BUILDING_IMG_OUT
from utils.utils import create_geo_json_from_polygon, get_features


def find_band_path(title, meter_subdirs=False):
    extracted_image_data_path = os.path.join(DOWNLOAD_DIRECTORY, title, f'{title}.SAFE', 'GRANULE', '*', 'IMG_DATA','*')
    if meter_subdirs:
        extracted_image_data_path = os.path.join(DOWNLOAD_DIRECTORY, title, f'{title}.SAFE', 'GRANULE', '*', 'IMG_DATA',
                                                 'R10m', '*')
    print(extracted_image_data_path)
    band2 = band3 = band4 = None
    for file_path in glob.glob(extracted_image_data_path):
        if 'B02' in os.path.basename(file_path):
            print(f'Band 2 file: {file_path}')
            band2 = rasterio.open(file_path, driver='JP2OpenJPEG')
        elif 'B03' in os.path.basename(file_path):
            print(f'Band 3 file: {file_path}')
            band3 = rasterio.open(file_path, driver='JP2OpenJPEG')
        elif 'B04' in os.path.basename(file_path):
            print(f'Band 4 file: {file_path}')
            band4 = rasterio.open(file_path, driver='JP2OpenJPEG')

    if not band2 or not band3 or not band4:
        raise FileNotFoundError('One or more bands are missing')

    return band2, band3, band4


def convert_image_to_tif(title):
    try:
        band2, band3, band4 = find_band_path(title)
    except FileNotFoundError as e:
        print(e)
        try:
            band2, band3, band4 = find_band_path(title, True)
        except FileNotFoundError as e:
            print(e)
    os.makedirs(TIF_IMAGE_DIRECTORY, exist_ok=True)
    true_color = rasterio.open(os.path.join(TIF_IMAGE_DIRECTORY, f'{title}.tif'), 'w', driver='Gtiff',
                               width=band4.width, height=band4.height,
                               count=3, crs=band4.crs, transform=band4.transform, dtype=band4.dtypes[0])
    true_color.write(band2.read(1), 3)
    true_color.write(band3.read(1), 2)
    true_color.write(band4.read(1), 1)
    true_color.close()


def crop_building_from_tif(buildings_df, title):
    # project = pyproj.Transformer.from_proj(
    #     pyproj.Proj('epsg:32634'),  # source coordinate system
    #     pyproj.Proj('epsg:4326'))  # destination coordinate system
    # geom = box(*bounds)
    # g2 = transform(project.transform, geom)
    # geo_json = create_geo_json_from_polygon(g2.wkt)
    # print(geo_json)
    for key, row in buildings_df.iterrows():
        # polygon = transform(project.transform, row['st_astext'])
        # print(polygon)



        geo_json = create_geo_json_from_polygon(row['st_astext'])
        # geo_json = BUILDING_IN_MUNICH_GEOJSON

        coords = get_features(geo_json)
        coords = rasterio.warp.transform_geom(
            CRS.from_epsg(4326),
            CRS.from_epsg(32632),
            coords
        )

        try:
            with rasterio.open(os.path.join(TIF_IMAGE_DIRECTORY, f'{title}.tif')) as src:
                out_img, out_transform = mask(src, shapes=coords, crop=True, pad_width=0.5)
                out_meta = src.meta.copy()

            out_meta.update({"driver": "GTiff", "height": out_img.shape[1], "width": out_img.shape[2],
                             "transform": out_transform})
            building_out_dir = os.path.join(BUILDING_IMG_OUT, str(key))
            os.makedirs(building_out_dir, exist_ok=True)
            building_out_img_path = os.path.join(building_out_dir, f'{title}-{key}.tif')
            with rasterio.open(building_out_img_path, "w", **out_meta) as dest:
                dest.write(out_img)
        except ValueError as e:
            print(e)
            continue
        exit()



def create_rgb_image_from_bands(title, buildings_df):
    convert_image_to_tif(title)
    crop_building_from_tif(buildings_df, title)

