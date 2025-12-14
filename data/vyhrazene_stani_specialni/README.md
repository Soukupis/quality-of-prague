# Vyhrazené Stání Speciální (Special Reserved Parking in Prague)

## Dataset Contents
- `vyhrazene_stani_specialni.geojson`: GeoJSON file containing the boundaries and properties of special reserved parking zones in Prague.

## Data Source
- Likely sourced from official Prague city geo portal: https://geoportalpraha.cz/data-a-sluzby/720a5804b9ef4c73af2d85f5605c1dc6

## Data Structure

| Field         | Description                                                      | Example Value                          |
|---------------|------------------------------------------------------------------|----------------------------------------|
| objectid      | Unique identifier for the parking zone                           | 65391                                  |
| zps_id        | Zone parking system identifier                                   | 2264                                   |
| id_poskyt     | Provider or administrative code                                  | 38                                     |
| shape_area_1  | Additional area measurement                                      | 0.0                                    |
| globalid      | Global unique identifier (UUID format)                           | {ED0B286D-46CE-4784-B2F3-3A2FCC6C7321} |
| shape_Length  | Perimeter length of the zone (degrees/meters)                    | 0.001209                               |
| shape_Area    | Area of the zone (square degrees/meters)                         | 1.2491931e-08                          |
| geometry      | Geometry type and coordinates (MultiPolygon WKT-style string)    | MULTIPOLYGON (((...)))                 |

### Example Record

| objectid | zps_id | id_poskyt | shape_area_1 | globalid                                 | shape_Length | shape_Area    | geometry           |
|----------|--------|-----------|--------------|------------------------------------------|--------------|---------------|--------------------|
| 65391    | 2264   | 38        | 0.0          | {ED0B286D-46CE-4784-B2F3-3A2FCC6C7321}   | 0.001209     | 1.2491931e-08 | MULTIPOLYGON ((...)) |

