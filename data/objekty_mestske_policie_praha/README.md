# Objekty Městské Policie Praha (Prague City Police Objects)

## Dataset Contents
- `objekty_mestske_policie_praha.geojson`: GeoJSON file containing locations and attributes of objects related to the Prague City Police (e.g., stations, facilities).

## Data Source
- Likely sourced from official Prague city geo portal: https://geoportalpraha.cz/data-a-sluzby/87f9881dab2847c09d6b1da7090d0f6c

## Data Structure

| Field      | Description                                                      | Example Value                |
|------------|------------------------------------------------------------------|------------------------------|
| objectid   | Unique identifier for the object                                 | 106                          |
| nku        | District or area name                                            | Nové Město                   |
| nvpk       | Street or location name                                          | Opletalova                   |
| cpop       | Building or address number (may be float or int)                 | 1441.0                       |
| pozn       | Note or description (e.g., type of facility)                     | OŘ MP Praha 1 / Služebna     |
| id_poskyt  | Provider or administrative code                                  | 301                          |
| or_mp      | Police district/department name                                  | OŘ MP Praha 1                |
| globalid   | Global unique identifier (UUID format)                           | {023C818E-F169-45A4-9174-BBAD540E9183} |
| geometry   | Geometry type and coordinates (WKT-style string)                 | POINT (14.43144 50.08266)    |

### Example Record

| objectid | nku         | nvpk         | cpop   | pozn            | id_poskyt | or_mp         | globalid                                 | geometry                   |
|----------|-------------|--------------|--------|-----------------|-----------|--------------|------------------------------------------|----------------------------|
| 106      | Nové Město  | Opletalova   | 1441.0 | OŘ MP Praha 1   | 301       | OŘ MP Praha 1| {023C818E-F169-45A4-9174-BBAD540E9183}   | POINT (14.43144 50.08266)  |
