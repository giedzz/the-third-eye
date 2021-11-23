import os

ZIP_OUTPUT_FOLDER = 'out/unzip_directory'
DOWNLOAD_DIRECTORY = 'data'
TIF_IMAGE_DIRECTORY = os.path.join(DOWNLOAD_DIRECTORY, 'tif_images')
BUILDING_IMG_OUT = 'data/tif_images/buildings/'


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
              11.756680011749268,
              48.102444781575464
            ],
            [
              11.756529808044434,
              48.102244168876844
            ],
            [
              11.756250858306885,
              48.10183577632125
            ],
            [
              11.756701469421387,
              48.10161366672713
            ],
            [
              11.756819486618042,
              48.10158500735476
            ],
            [
              11.75705552101135,
              48.101864435553814
            ],
            [
              11.757280826568604,
              48.10216535653107
            ],
            [
              11.756969690322876,
              48.10233014584356
            ],
            [
              11.756680011749268,
              48.102444781575464
            ]
          ]
        ]
      }
    }
  ]
}