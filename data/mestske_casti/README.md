# Městské části (Prague Districts)

## Dataset Contents
- `mestske_casti.geojson`: GeoJSON file containing the boundaries and properties of Prague's municipal districts (městské části).

## Data Source
- Likely sourced from official Prague city geo portal: https://geoportalpraha.cz/data-a-sluzby/2ce0a7a48eb542fb858a998f77a5b227

## Data Structure

| Field         | Description                                                      | Example Value                |
|---------------|------------------------------------------------------------------|------------------------------|
| objectid      | Unique identifier for the district                               | 1                            |
| kod_mc        | District code                                                    | 539449                       |
| nazev_mc      | District name                                                    | Praha-Lipence                |
| poskyt        | Data provider                                                    | HMP-IPR                      |
| id_poskyt     | Provider code                                                    | 43                           |
| nazev_1       | District name (short/alternative)                                | Lipence                      |
| globalid      | Global unique identifier (UUID format)                           | {4241F642-D542-418C-8A51-D4FE4F2AA07F} |
| shape_Length  | Perimeter length of the district (degrees/meters)                | 0.161585                     |
| shape_Area    | Area of the district (square degrees/meters)                     | 0.001033                     |
| geometry      | Geometry type and coordinates (MultiPolygon WKT-style string)    | MULTIPOLYGON (((...)))       |

### Example Record

| objectid | kod_mc | nazev_mc      | poskyt  | id_poskyt | nazev_1   | globalid                                 | shape_Length | shape_Area | geometry                |
|----------|--------|--------------|---------|-----------|-----------|------------------------------------------|--------------|------------|-------------------------|
| 1        | 539449 | Praha-Lipence| HMP-IPR | 43        | Lipence   | {4241F642-D542-418C-8A51-D4FE4F2AA07F}  | 0.161585     | 0.001033   | MULTIPOLYGON (((...)))  |
