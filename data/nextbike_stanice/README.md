# Nextbike Stanice (Prague Bike-Sharing Stations)

## Dataset Contents
- `nextbike_stanice.geojson`: GeoJSON file containing locations and attributes of Nextbike bike-sharing stations in Prague.

## Data Source
- Nextbike GBFS v2.3 open feed: https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_tg/cs/station_information.json
- GBFS autodiscovery endpoint: https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_tg/gbfs.json
- Data retrieved: 2026-06-09
- License: General Bikeshare Feed Specification (GBFS) open data

## Data Structure

| Field             | Description                                               | Example Value         |
|-------------------|-----------------------------------------------------------|-----------------------|
| station_id        | Unique Nextbike station identifier                        | 27581946              |
| name              | Station name (format: P{district}-{location name})       | P10-Čechovo náměstí   |
| short_name        | Short numeric station code                                | 46007                 |
| capacity          | Number of bike docking slots at the station               | 10                    |
| region_id         | Nextbike regional network identifier (661 = Prague)       | 661                   |
| is_virtual_station| Whether station is virtual (no physical docking)          | false                 |
| geometry          | Point geometry (WGS84 / EPSG:4326)                        | POINT (14.47, 50.07)  |

### Example Record

| station_id | name                   | short_name | capacity | region_id | is_virtual_station | geometry                    |
|------------|------------------------|------------|----------|-----------|--------------------|-----------------------------|
| 27581946   | P10-Čechovo náměstí    | 46007      | 10       | 661       | false              | POINT (14.4812, 50.0624)    |

## Notes
- 217 stations filtered to Prague (region_id 661 or station name prefix P1–P22)
- Station names use format `P{district number}-{location}` enabling approximate district assignment
- QoL relevance: QOUL Mobility domain — bike-sharing as sustainable last-mile transport; supports 15-Minute City accessibility and reduced car dependence
