--Query to find building higher than 30m bounded in bounding box of 4326 coordinates (bounding box is close to Europe borders)
SELECT ST_Transform(way, 4326 ), *
FROM planet_osm_polygon
WHERE planet_osm_polygon.way && ST_Transform(
  ST_MakeEnvelope(-10.239, 58.995, 36.431, 36.95, 4326),3857
) and (tags -> 'height') ~ E'^\\d+$' and (tags -> 'height')::float > 30
LIMIT 100