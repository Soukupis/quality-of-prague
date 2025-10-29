# Parkovací Automaty (Parking Meters in Prague)

## Dataset Contents
- `parkovaci_automaty.geojson`: GeoJSON file containing the locations and attributes of parking meters in Prague.

## Data Source
- Likely sourced from official Prague city geo portal: https://geoportalpraha.cz/data-a-sluzby/2b49ad1ad0bb4892bcb54acfb978456a
## Data Structure

| Field      | Description                                              | Example Value                          |
|------------|----------------------------------------------------------|----------------------------------------|
| objectid   | Unique identifier for the parking meter                  | 62473                                  |
| id_poskyt  | Provider or administrative code                          | 38                                     |
| globalid   | Global unique identifier (UUID format)                   | {A5FCEFE1-27F9-475B-A9AF-DAAE837D200D} |
| pa         | Parking meter code                                       | 22000004                               |
| px         | Parking zone code                                        | P22                                    |
| street     | Street name (may include additional info in parentheses) | Františka Diviše (nn7461)              |
| code       | Numeric code for the parking meter                       | 22000004                               |
| geometry   | Geometry type and coordinates (WKT-style string)         | POINT (14.596343266, 50.031047546)     |

### Example Record

| objectid | id_poskyt | globalid                                 | pa       | px  | street                     | code      | geometry                   |
|----------|-----------|------------------------------------------|----------|-----|----------------------------|-----------|----------------------------|
| 62473    | 38        | {A5FCEFE1-27F9-475B-A9AF-DAAE837D200D}   | 22000004 | P22 | Františka Diviše (nn7461)  | 22000004  | POINT (14.596343266, 50.031047546) |

