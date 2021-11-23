import pandas as pd

pg_out = pd.read_csv('pgAdminResults/limit_10000_test.csv')
max_long = -99999
max_long_coordinates = None
max_lat = -99999
max_lat_coordinates = None
min_long = 99999
min_long_coordinates = None
min_lat = 99999
min_lat_coordinates = None
for key, row in pg_out.iterrows():
    row_formatted = row['st_astext'].replace('POLYGON((', '').replace('))', '').replace('(', '').replace(')', '').split(',')
    for coordinates in row_formatted:
        coordinates = coordinates.split(' ')
        long = float(coordinates[0])
        lat = float(coordinates[1])
        if long > max_long:
            max_long = long
            max_long_coordinates = coordinates
        if lat > max_lat:
            max_lat = lat
            max_lat_coordinates = coordinates
        if long < min_long:
            min_long = long
            min_long_coordinates = coordinates
        if lat < min_lat:
            min_lat = lat
            min_lat_coordinates = coordinates
print(max_long_coordinates)
print(max_lat_coordinates)
print(min_long_coordinates)
print(min_lat_coordinates)
