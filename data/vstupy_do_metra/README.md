# Vstupy do Metra (Prague Metro Entrances)

## Dataset Contents
- `vstupy_do_metra.geojson`: GeoJSON file containing locations and attributes of metro station entrances in Prague.

## Data Source
- Likely sourced from official Prague city geo portal: https://geoportalpraha.cz/data-a-sluzby/62106cae6acf4507b988c0e745f55bba

## Data Structure

| Field       | Description                                                      | Example Value                          |
|-------------|------------------------------------------------------------------|----------------------------------------|
| objectid    | Unique identifier for the metro entrance                         | 1                                      |
| uzel_nazev  | Station node name                                                | Opatov                                 |
| vest_nazev  | Vestibule name                                                   | Opatov                                 |
| vst_popis   | Entrance description (destinations, connections)                 | E1 BUS Litochlebsk nm., Chodovec, ... |
| id_poskyt   | Provider or administrative code                                  | null                                   |
| globalid    | Global unique identifier (UUID format)                           | {9F59BA7D-00BB-49F8-96F2-C414CA3AEB45} |
| vst_linka   | Metro line identifier (A, B, or C)                               | C                                      |
| vst_nazev   | Entrance name                                                    | E1 BUS Litochlebsk nměst               |
| uzel_cislo  | Station node number                                              | 106                                    |
| vst_kod     | Entrance code                                                    | 1                                      |
| vest_kod    | Vestibule code                                                   | 1                                      |
| vst_mim_od  | Out-of-service start date (if applicable)                        | null                                   |
| vst_mim_do  | Out-of-service end date (if applicable)                          | null                                   |
| vst_schod   | Stairs availability (0=no, 1=yes, 2=yes, 3=yes)                  | 1                                      |
| vst_eskal   | Escalator availability (0=no, 1=yes, 2=yes, 3=yes)              | 1                                      |
| vst_vytah   | Elevator/lift availability (0=no, 1=yes, 2=yes)                 | 0                                      |
| vst_oznac   | Entrance designation/label                                       | E1                                     |
| geometry    | Geometry type and coordinates (WKT-style string)                 | POINT (14.508280006, 50.028080005)    |

### Example Record

| objectid | uzel_nazev | vest_nazev | vst_popis                                              | vst_linka | vst_nazev                | uzel_cislo | vst_kod | vst_schod | vst_eskal | vst_vytah | vst_oznac | geometry                         |
|----------|------------|------------|--------------------------------------------------------|-----------|--------------------------|------------|---------|-----------|-----------|-----------|-----------|----------------------------------|
| 1        | Opatov     | Opatov     | E1 BUS Litochlebsk nm., Chodovec, Spořilov, Na Košku  | C         | E1 BUS Litochlebsk nměst | 106        | 1       | 1         | 1         | 0         | E1        | POINT (14.508280006, 50.028080005) |