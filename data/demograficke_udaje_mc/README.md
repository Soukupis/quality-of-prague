# Demografické Údaje Městských Částí (Prague District Demographic Statistics)

## Dataset Contents
- `demograficke_udaje_mc.xlsx`: Excel workbook with annual demographic and socio-economic statistics for all 57 Prague city districts (městské části). Each sheet corresponds to one year (2004–2025).

## Data Source
- Czech Statistical Office (ČSÚ): https://csu.gov.cz/docs/107839/4473deb4-e987-202b-1e15-740fcaccfba3/Casova_rada_MC.xlsx
- Published by: Český statistický úřad (ČSÚ)
- Data retrieved: 2026-06-09
- Last updated: 2026-04-13 (data for 2025 being added throughout 2026)
- License: Open data (CC BY 4.0)

## Data Structure

The workbook contains one sheet per year (2004–2025). Each sheet has:
- **Row 1**: Title row (year label)
- **Row 2**: Last updated date
- **Row 3**: Column headers — column A = indicator name, columns B onwards = district names (Hl. m. Praha, Praha 1, Praha 2, … all 57 districts)

Key indicators (row labels in column A):

| Indicator (Czech/English)                                      | Example Value (Praha 1, 2024) |
|----------------------------------------------------------------|-------------------------------|
| Rozloha (ha) / Area (hectares)                                 | 553.84                        |
| Hustota zalidnění (osoby/km²) / Population density            | 5 221.9                       |
| Počet obyvatel k 31. 12. / Population as at 31 December        | 28 921                        |
| z toho ženy / incl. Females                                    | 13 435                        |
| Podíl 0–14 / Population aged 0–14 (%)                         | 11.6%                         |
| Podíl 15–64 / Population aged 15–64 (%)                       | 71.4%                         |
| Podíl 65+ / Population aged 65+ (%)                           | 17.0%                         |
| Průměrný věk / Mean age (years)                                | 43.3                          |
| Živě narození / Live births                                    | 221                           |
| Zemřelí / Deaths                                               | 222                           |
| Přirozený přírůstek / Natural increase                         | –1                            |
| Stěhování — přistěhovalí / Net migration (in)                  | varies                        |

### Example Record (Praha 1, sheet "2024")

| Indicator                   | Praha 1 (2024) |
|-----------------------------|----------------|
| Area (ha)                   | 553.84         |
| Population density (p/km²)  | 5 221.9        |
| Total population            | 28 921         |
| Female population           | 13 435         |
| Age 0–14 (%)                | 11.6           |
| Age 65+ (%)                 | 17.0           |
| Mean age                    | 43.3           |

## Notes
- Time series from 2004 to 2025 enables longitudinal analysis of demographic change per district
- Population data enables per-capita normalization of all other spatial indicators (e.g., police stations per 1000 residents)
- Age structure (65+) critical for Jan persona analysis (barrier-free infrastructure demand) and elderly population vulnerability to urban heat islands
- QoL relevance: QOUL Socio-economic Security domain; OECD Better Life Index denominator for per-capita indicators; Stiglitz-Sen-Fitoussi recommendation for population-weighted metrics
