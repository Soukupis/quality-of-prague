# Vyhrazené Stání pro Zásobování (Reserved Parking for Supply/Delivery in Prague)

## Dataset Contents
- `vyhrazene_stani_pro_zasobovani.geojson`: GeoJSON file containing locations and boundaries of reserved parking/standing areas for supply and delivery vehicles in Prague.

## Data Source
- Likely sourced from official Prague city geo portal: https://geoportalpraha.cz/data-a-sluzby/b62d8490d0034b55b2982386a5d1027c

## Data Structure

| Field         | Description                                                      | Example Value                          |
|---------------|------------------------------------------------------------------|----------------------------------------|
| objectid      | Unique identifier for the reserved parking area                  | 62086                                  |
| zps_id        | Reserved parking zone ID                                         | 2027                                   |
| id_poskyt     | Provider or administrative code                                  | 38                                     |
| shape_area_1  | Alternative area field (typically 0.0)                           | 0.0                                    |
| globalid      | Global unique identifier (UUID format)                           | {3183F302-DBFA-451F-BFEB-41EE5F9303AE} |
| shape_Length  | Perimeter length of the parking area (degrees)                   | 0.00036142900211553488                 |
| shape_Area    | Area of the parking zone (square degrees)                        | 3.6653000520488178e-09                 |
| geometry      | Geometry type and coordinates (MultiPolygon WKT-style string)    | MULTIPOLYGON (((14.345..., 50.098...)))|

### Example Record

| objectid | zps_id | id_poskyt | shape_area_1 | globalid                                 | shape_Length           | shape_Area              | geometry                |
|----------|--------|-----------|--------------|------------------------------------------|------------------------|-------------------------|-------------------------|
| 62086    | 2027   | 38        | 0.0          | {3183F302-DBFA-451F-BFEB-41EE5F9303AE}   | 0.00036142900211553488 | 3.6653000520488178e-09  | MULTIPOLYGON (((...)))  |

