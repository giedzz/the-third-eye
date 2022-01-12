import pandas as pd
import shapely.wkt
from shapely.geometry import MultiPoint, LineString
from shapely.ops import transform
from functools import partial
import pyproj


def get_measurements_in_meters(measure_line):
    project = partial(
        pyproj.transform,
        pyproj.Proj('EPSG:4326'),
        pyproj.Proj('EPSG:32633'))
    measure_line_transformed = transform(project, measure_line)
    # print(str(width.length) + " meters")
    return measure_line_transformed.length


def get_min_max_long_lat(_coords_bbox):
    _min_long = min(_coords_bbox[0], _coords_bbox[2])
    _max_long = max(_coords_bbox[0], _coords_bbox[2])
    _min_lat = min(_coords_bbox[1], _coords_bbox[3])
    _max_lat = max(_coords_bbox[1], _coords_bbox[3])
    return _min_long, _max_long, _min_lat, _max_lat


def get_width_length(polygon_row, width_measure):
    current_polygon = shapely.wkt.loads(polygon_row)
    coords = current_polygon.exterior.coords
    coords_bbox = MultiPoint(list(coords)).bounds
    min_long, max_long, min_lat, max_lat = get_min_max_long_lat(coords_bbox)
    width_line = LineString([(min_long, min_lat), (min_long, max_lat)])
    length_line = LineString([(min_long, min_lat), (max_long, min_lat)])
    width = get_measurements_in_meters(width_line)
    length = get_measurements_in_meters(length_line)
    if width_measure:
        return width
    else:
        return length


def main():
    input_fp = 'pgAdminResults/20m_limit_100000_v2.csv'
    output_fp = 'pgAdminResultsFiltered/20m_limit_100000_v2_filtered.csv'
    pg_out = pd.read_csv(input_fp)

    # Limits are in meters
    MIN_FILTER_LIMIT = 40
    MAX_FILTER_LIMIT = 100
    pg_out['width'] = pg_out['st_astext'].apply(get_width_length, width_measure=True)
    pg_out['length'] = pg_out['st_astext'].apply(get_width_length, width_measure=False)
    pg_out_filtered = pg_out.query(f'(width > {MIN_FILTER_LIMIT} & length > {MAX_FILTER_LIMIT}) |'
                                   f' (width > {MAX_FILTER_LIMIT} & length > {MIN_FILTER_LIMIT})')
    pg_out_filtered_reset = pg_out_filtered.reset_index(drop=True)
    pg_out_filtered_reset.to_csv(output_fp)


if __name__ == "__main__":
    main()
