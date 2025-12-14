# Úseky Placeného Stání (Paid Parking Zones in Prague)

## Dataset Contents
- `useky_placeneho_stani.geojson`: GeoJSON file containing the boundaries and attributes of paid parking zones in Prague.

## Data Source
- Likely sourced from official Prague city geo portal: https://geoportalpraha.cz/data-a-sluzby/7cbfdf9f9d87418ba62b35762cd46ca7

## Data Structure

| Field         | Description                                                      | Example Value                          |
|---------------|------------------------------------------------------------------|----------------------------------------|
| objectid      | Unique identifier for the parking zone segment                   | 371801                                 |
| zps_id        | Paid parking zone ID                                             | 2028                                   |
| typzony       | Zone type (1=purple zone, 2=orange zone)                         | 1                                      |
| id_poskyt     | Provider or administrative code                                  | 38                                     |
| tariftab      | Tariff table code                                                | P6-0138                                |
| ps_zps        | Number of parking spaces in the zone segment                     | 14                                     |
| shape_area_1  | Additional area measurement                                      | 0.0                                    |
| globalid      | Global unique identifier (UUID format)                           | {3594C227-B619-4D6E-BCF4-99C939BA5CFF} |
| shape_Length  | Perimeter length of the zone segment (degrees/meters)            | 0.0028730816741564863                  |
| shape_Area    | Area of the zone segment (square degrees/meters)                 | 2.5387622880946321e-08                 |
| geometry      | Geometry type and coordinates (MultiPolygon WKT-style string)    | MULTIPOLYGON (((...)))                 |

### Example Record

| objectid | zps_id | typzony | id_poskyt | tariftab | ps_zps | globalid                                 | shape_Length         | shape_Area              | geometry                |
|----------|--------|---------|-----------|----------|--------|------------------------------------------|----------------------|-------------------------|-------------------------|
| 371801   | 2028   | 1       | 38        | P6-0138  | 14     | {3594C227-B619-4D6E-BCF4-99C939BA5CFF}  | 0.002873081674...    | 2.538762288e-08         | MULTIPOLYGON (((...)))  |

### Zone Types
- **Type 1 (Purple Zone)**: Primarily for residents and visitors with permits
- **Type 2 (Orange Zone)**: Mixed-use zones with different tariffs

