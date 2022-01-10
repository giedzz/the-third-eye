import os

ZIP_OUTPUT_FOLDER = 'out/unzip_directory'
DOWNLOAD_DIRECTORY = 'data'
TIF_IMAGE_DIRECTORY = os.path.join(DOWNLOAD_DIRECTORY, 'tif_images')
BUILDING_IMG_OUT = 'data/rgb_images/buildings/'
RASTER_INFO_TXT_PTH = 'data/txt_files'

OUTPUT_BUILDING_PNG_PATH = 'data/tif_images/buildings_jpg/'


BUILDING_IN_MUNICH_GEOJSON = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              11.729621887207031,
              48.33525610652687
            ],
            [
              11.810646057128906,
              48.33525610652687
            ],
            [
              11.810646057128906,
              48.37039155719172
            ],
            [
              11.729621887207031,
              48.37039155719172
            ],
            [
              11.729621887207031,
              48.33525610652687
            ]
          ]
        ]
      }
    }
  ]
}