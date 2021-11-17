from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

api = SentinelAPI('thethirdeye', 'thethirdeye123', 'https://scihub.copernicus.eu/dhus')

# search by polygon, time, and SciHub query keywords
footprint = geojson_to_wkt(read_geojson('example.geojson'))
products = api.query(footprint,
                     platformname='Sentinel-2',
                     cloudcoverpercentage=(0, 30))
for key, value in products.items():
    # download single scene by known product id
    # Try except implemented to exit only if we have downloaded image, if not print error and continue
    # Further steps would include unzipping downloaded image and creating images for classification training
    try:
        api.download(key)
    except Exception as e:
        print(e)
        continue
    exit()
