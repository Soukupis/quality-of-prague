# Zákaz Stání (No Parking Zones in Prague)

## Dataset Contents
- `zakaz_stani.geojson`: GeoJSON file containing the boundaries and properties of no parking zones in Prague.

## Data Source
- Likely sourced from official Prague city geo portal: https://geoportalpraha.cz/data-a-sluzby/b2be4777cec1443fa1e9b4b0d385fed1

## Data Structure

| Field         | Description                                                      | Example Value                          |
|---------------|------------------------------------------------------------------|----------------------------------------|
| objectid      | Unique identifier for the no parking zone                        | 347394                                 |
| zps_id        | Zone parking system identifier                                   | 2029                                   |
| id_poskyt     | Provider or administrative code                                  | 38                                     |
| shape_area_1  | Additional area measurement                                      | 0.0                                    |
| globalid      | Global unique identifier (UUID format)                           | {29247E35-861C-408C-B753-0B6FAD2E34DC} |
| shape_Length  | Perimeter length of the zone (degrees/meters)                    | 0.000338                               |
| shape_Area    | Area of the zone (square degrees/meters)                         | 2.5198718e-09                          |
| geometry      | Geometry type and coordinates (MultiPolygon WKT-style string)    | MULTIPOLYGON (((...)))                 |

### Example Record

| objectid | zps_id | id_poskyt | shape_area_1 | globalid                                 | shape_Length | shape_Area    | geometry           |
|----------|--------|-----------|--------------|------------------------------------------|--------------|---------------|--------------------|
| 347394   | 2029   | 38        | 0.0          | {29247E35-861C-408C-B753-0B6FAD2E34DC}   | 0.000338     | 2.5198718e-09 | MULTIPOLYGON ((...)) |


