# Parking P+R (Park and Ride Facilities in Prague)

## Dataset Contents
- `parking_p_r.geojson`: GeoJSON file containing the locations and properties of Park and Ride (P+R) parking facilities in Prague.

## Data Source
- Likely sourced from official Prague city geo portal: https://geoportalpraha.cz/data-a-sluzby/7dce241cdbb141fa8104e3a65ca67ad6

## Data Structure

| Field           | Description                                              | Example Value                          |
|-----------------|----------------------------------------------------------|----------------------------------------|
| objectid        | Unique identifier for the parking facility               | 1                                      |
| typ             | Type of parking facility (1-5)                           | 1                                      |
| stav            | Status/condition of the facility (1, 4, or 5)            | 1                                      |
| nazev           | Name of the parking facility                             | Běchovice                              |
| kapacita        | Current capacity (number of parking spaces)              | 92                                     |
| kapacita_vyhled | Future/planned capacity (number of parking spaces)       | 300                                    |
| id_poskyt       | Provider or administrative code                          | 43                                     |
| globalid        | Global unique identifier (UUID format)                   | {57EEF6EF-C311-454C-8B7F-8A01D413D1BE} |
| geometry        | Geometry type and coordinates (WKT-style string)         | POINT (14.596779481, 50.080758754)    |

### Example Record

| objectid | typ | stav | nazev      | kapacita | kapacita_vyhled | id_poskyt | globalid                                 | geometry                           |
|----------|-----|------|------------|----------|-----------------|-----------|------------------------------------------|------------------------------------|
| 1        | 1   | 1    | Běchovice  | 92       | 300             | 43        | {57EEF6EF-C311-454C-8B7F-8A01D413D1BE}   | POINT (14.596779481, 50.080758754) |


