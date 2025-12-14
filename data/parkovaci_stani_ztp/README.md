# Parkovací Stání ZTP (Disabled Parking Spaces in Prague)

## Dataset Contents
- `parkovaci_stani_ztp.geojson`: GeoJSON file containing the locations and attributes of disabled parking spaces (ZTP - zdravotně těžce postižení) in Prague.

## Data Source
- Likely sourced from official Prague city geo portal: https://geoportalpraha.cz/data-a-sluzby/ab4a8cd8fc284b738ca806681559d694

## Data Structure

| Field        | Description                                              | Example Value                          |
|--------------|----------------------------------------------------------|----------------------------------------|
| objectid     | Unique identifier for the parking space                  | 1                                      |
| pocet_ps     | Number of parking spaces                                 | 1                                      |
| rozm_delka   | Length dimension in meters                               | 4.5                                    |
| rozm_sirka   | Width dimension in meters                                | 2.5                                    |
| typ_ps       | Type of parking space (1-5)                              | 3                                      |
| kolme_ps     | Perpendicular parking indicator (1=yes, 2=no)            | 2                                      |
| pod_sklon    | Longitudinal slope in percent                            | 0.0                                    |
| pric_sklon   | Transverse slope in percent                              | 0.0                                    |
| typ_povrch   | Type of surface (1-3)                                    | 1                                      |
| posk_povrc   | Surface damage level (1-2)                               | 2                                      |
| pes_zona     | Pedestrian zone indicator                                | 2                                      |
| mat_povrch   | Surface material (1-7)                                   | 1                                      |
| id_poskyt    | Provider or administrative code                          | 38                                     |
| globalid     | Global unique identifier (UUID format)                   | {B0AF6B19-B810-4FB9-BD7F-CF8508F0C768} |
| geometry     | Geometry type and coordinates                            | Point (14.470924961, 50.058871778)     |

### Example Record

| objectid | pocet_ps | rozm_delka | rozm_sirka | typ_ps | kolme_ps | pod_sklon | pric_sklon | typ_povrch | posk_povrc | pes_zona | mat_povrch | id_poskyt | globalid                                 | geometry                           |
|----------|----------|------------|------------|--------|----------|-----------|------------|------------|------------|----------|------------|-----------|------------------------------------------|------------------------------------|
| 1        | 1        | 4.5        | 2.5        | 3      | 2        | 0.0       | 0.0        | 1          | 2          | 2        | 1          | 38        | {B0AF6B19-B810-4FB9-BD7F-CF8508F0C768}   | POINT (14.470924961, 50.058871778) |

