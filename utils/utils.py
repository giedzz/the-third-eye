import os
import shutil
import zipfile

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
        long = float(parsed_coordinate[0])
        lat = float(parsed_coordinate[1])
        geojson['features'][0]['geometry']['coordinates'][0].append([lat, long])
    return geojson


def get_features(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    print(gdf)
    return [gdf['features'][0]['geometry']]


def delete_created_files(title):
    # Remove zip file
    os.remove(os.path.join(DOWNLOAD_DIRECTORY, f'{title}.zip'))
    # Remove extracted files
    shutil.rmtree(os.path.join(DOWNLOAD_DIRECTORY, title))
    # Remove tif image
    os.remove(os.path.join(TIF_IMAGE_DIRECTORY, f'{title}.tif'))


