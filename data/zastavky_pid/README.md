# Zastávky PID (Prague Integrated Transport Stops)

## Dataset Contents
- `zastavky_pid.geojson`: GeoJSON file containing locations and attributes of all public transport stops within Prague (Pražská integrovaná doprava — PID network).

## Data Source
- PID open data portal: https://data.pid.cz/stops/json/stops.json
- Published by: Ropid — Regionální organizátor Pražské integrované dopravy
- Data retrieved: 2026-06-09
- License: CC BY 4.0

## Data Structure

| Field         | Description                                                                | Example Value   |
|---------------|----------------------------------------------------------------------------|-----------------|
| stop_id       | Unique stop identifier (format: {node}/{platform})                         | 876/1           |
| stop_name     | Name of the stop group / station                                           | Albertov        |
| platform      | Platform designation within the stop group                                 | A               |
| zone          | Tariff zone identifier (P = central Prague, B–9 = outer zones)             | P               |
| traffic_type  | Mode of transport: metro, tram, bus, train, ferry, funicular               | tram            |
| wheelchair    | Wheelchair accessibility: yes / possible / no / unknown                    | possible        |
| municipality  | Municipality name                                                          | Praha           |
| district_code | District code (AB = Praha)                                                 | AB              |
| geometry      | Point geometry (WGS84 / EPSG:4326)                                         | POINT (14.42, 50.07) |

### Example Record

| stop_id | stop_name  | platform | zone | traffic_type | wheelchair | municipality | district_code | geometry                      |
|---------|------------|----------|------|--------------|------------|--------------|---------------|-------------------------------|
| 876/1   | Albertov   | A        | P    | tram         | possible   | Praha        | AB            | POINT (14.4208, 50.0713)      |

## Notes
- 3,609 stop platforms across all modes (metro, tram, bus, train, ferry)
- Filtered to Praha municipality only (municipality = "Praha" or districtCode = "AB")
- Wheelchair accessibility field enables barrier-free transport analysis
- QoL relevance: QOUL Mobility domain — public transport coverage (15-Minute City proximity); WHOQOL Level of Independence — wheelchair-accessible stops for reduced-mobility residents
