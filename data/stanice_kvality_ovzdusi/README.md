# Stanice Kvality Ovzduší (Prague Air Quality Monitoring Stations)

## Dataset Contents
- `stanice_kvality_ovzdusi.geojson`: GeoJSON file containing locations and metadata of active air quality monitoring stations operated by ČHMÚ (Czech Hydrometeorological Institute) within Prague.

## Data Source
- ČHMÚ OpenData: https://opendata.chmi.cz/air_quality/recent/metadata/metadata.json
- Published by: Český hydrometeorologický ústav (ČHMÚ)
- Data retrieved: 2026-06-09
- License: Open data (CC BY 4.0)

## Data Structure

| Field        | Description                                                          | Example Value            |
|--------------|----------------------------------------------------------------------|--------------------------|
| station_code | Unique ČHMÚ station code                                             | AREP                     |
| name         | Station name including district                                      | Praha 1-n. Republiky     |
| active       | Whether the station is currently active                              | true                     |
| station_type | EOI station type: pozaďová (background), dopravní (traffic), průmyslová (industrial) | pozaďová |
| zone_type    | EOI zone type: městská (urban), příměstská (suburban), venkovská (rural) | městská  |
| city         | City/locality name                                                   | Praha 2                  |
| street       | Street address of the station                                        | Legerova                 |
| region       | Czech administrative region                                          | Praha                    |
| geometry     | Point geometry (WGS84 / EPSG:4326)                                   | POINT (14.43, 50.08)     |

### Example Record

| station_code | name                    | active | station_type | zone_type | city     | street   | geometry                  |
|--------------|-------------------------|--------|--------------|-----------|----------|----------|---------------------------|
| AREP         | Praha 1-n. Republiky    | true   | pozaďová     | městská   |          |          | POINT (14.4302, 50.0874)  |
| ALEG         | Praha 2-Legerova        | true   | dopravní     | městská   | Praha 2  | Legerova | POINT (14.4363, 50.0747)  |

## Notes
- 14 active Prague monitoring stations extracted from the nationwide metadata file (98 total stations across Czech Republic)
- Pollutants measured vary by station but include: PM2.5, PM10, NO₂, O₃, SO₂, CO, benzene
- Actual measurement data available per-station at: https://opendata.chmi.cz/air_quality/recent/{station_code}/
- QoL relevance: QOUL Environmental Health domain — PM2.5, PM10, NO₂ exposure; WHOQOL Environment domain; Novák family persona (Dejvice/Evropská traffic pollution)
