# Parky Praha (Prague Parks and Green Spaces)

## Dataset Contents
- `parky_praha.geojson`: GeoJSON file containing centroid points of parks and green spaces in Prague, sourced from OpenStreetMap via the Overpass API.

## Data Source
- OpenStreetMap via Overpass API: https://overpass-api.de/api/interpreter
- Query: `way/relation["leisure"="park"]` within Prague bounding box (49.94°N–50.18°N, 14.22°E–14.71°E)
- Data retrieved: 2026-06-09
- License: OpenStreetMap data © OpenStreetMap contributors, ODbL 1.0

## Data Structure

| Field       | Description                                                         | Example Value             |
|-------------|---------------------------------------------------------------------|---------------------------|
| osm_id      | OpenStreetMap element ID                                            | 17681087                  |
| osm_type    | OSM element type: way (simple polygon) or relation (multipolygon)   | way                       |
| name        | Park name (null for unnamed green spaces)                           | Čakovický zámecký park    |
| leisure     | OSM leisure tag value (always "park" in this dataset)               | park                      |
| access      | Public access: yes / private / permissive / unknown                 | yes                       |
| operator    | Operating organization (if available)                               | null                      |
| wikipedia   | Wikipedia article link (if available)                               | null                      |
| geometry    | Centroid point geometry (WGS84 / EPSG:4326)                         | POINT (14.52, 50.17)      |

### Example Record

| osm_id   | osm_type | name                    | leisure | access | geometry                  |
|----------|----------|-------------------------|---------|--------|---------------------------|
| 17681087 | way      | Čakovický zámecký park  | park    | yes    | POINT (14.5180, 50.1681)  |
| 26870953 | way      | Stromovka                | park    | yes    | POINT (14.4148, 50.1044)  |

## Notes
- 1,054 total park features; 209 with names (remaining are unnamed public green spaces)
- Geometry is centroid point; original polygon boundaries available via OSM Overpass if needed
- OSM coverage is community-maintained and may miss newly created or very small green spaces
- Does not include: forests (landuse=forest), meadows, or private gardens — only tagged leisure=park
- QoL relevance: QOUL Environmental Health domain — proximity to green space is linked to mental well-being (Diener's bottom-up SWB model), reduced urban heat island effect, recreational accessibility; 15-Minute City "Fun" social function; WHOQOL Physical domain (outdoor activity)
