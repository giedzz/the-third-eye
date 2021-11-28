import os
import shutil
import zipfile

import shapely.wkt
from shapely.geometry import Polygon

from constants import DOWNLOAD_DIRECTORY, TIF_IMAGE_DIRECTORY


def unzip_file(title):
    zip_output_path = os.path.join(DOWNLOAD_DIRECTORY, title)
    zip_file_path = os.path.join(DOWNLOAD_DIRECTORY, f'{title}.zip')
    os.makedirs(zip_output_path, exist_ok=True)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(zip_output_path)


def create_geo_json_from_polygon(polygon_coordinates):
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[]]
                }
            }
        ]
    }
    parsed_coordinates = polygon_coordinates.replace('POLYGON ((', '').replace('))', '').replace('(', '').replace(')', '')
    parsed_coordinates = parsed_coordinates.replace('POLYGON', '')
    parsed_coordinates = parsed_coordinates.replace(', ', ',')
    parsed_coordinates = parsed_coordinates.split(',')
    for parsed_coordinate in parsed_coordinates:
        parsed_coordinate = parsed_coordinate.split(' ')
        if len(parsed_coordinate) < 2:
            parsed_coordinate = parsed_coordinate.split(',')
        long = float(parsed_coordinate[1])
        lat = float(parsed_coordinate[0])
        geojson['features'][0]['geometry']['coordinates'][0].append([lat, long])
    return geojson


def get_features(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    return [gdf['features'][0]['geometry']]


def delete_created_files(title):
    print(f'Deleting {title} files...')
    # Remove zip file
    os.remove(os.path.join(DOWNLOAD_DIRECTORY, f'{title}.zip'))
    # Remove extracted files
    shutil.rmtree(os.path.join(DOWNLOAD_DIRECTORY, title))
    # Remove tif image
    # os.remove(os.path.join(TIF_IMAGE_DIRECTORY, f'{title}.tif'))
    print(f'Files for {title} deleted.')

def sentinel_image_overlap_at_least_one_building(buildings_df, unformatted_multipol):
    multipol = shapely.wkt.loads(unformatted_multipol)
    for polygon in multipol:
        for key, row in buildings_df.iterrows():
            geo_json = create_geo_json_from_polygon(row['st_astext'])
            # geo_json = BUILDING_IN_MUNICH_GEOJSON
            coords = get_features(geo_json)
            p1 = Polygon(coords[0]['coordinates'][0])
            p2 = polygon
            if p1.intersects(p2):
                return True
    return False


def read_already_downloaded_sentinel_data_titles(fp):
    # define an empty list
    places = []
    # open file and read the content in a list
    with open(fp, 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]
            # add item to the list
            places.append(currentPlace)
    return places


def write_already_downloaded_sentinel_data_titles(fp, places_list):
    with open(fp, 'w') as filehandle:
        for listitem in places_list:
            filehandle.write('%s\n' % listitem)
