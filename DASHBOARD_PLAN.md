# Quality of Prague — Dashboard Plan

## 1. Theoretical Framework Summary

Source: *"Analysis of Factors Influencing Quality of Life in an Urban Environment: A Case Study of Prague Using Urban Planning Data"* — Bc. Joseph Meurer, Unicorn Vysoká Škola s.r.o. (Master Thesis Draft)

### Core QoL Dimensions

The thesis builds a four-layer theoretical framework:

#### Layer 1 — WHOQOL 6-Domain Model (WHO)
Individual-level clinical instrument; 24 facets across six domains. Most relevant urban domains:

| Domain | Key Urban Facets |
|---|---|
| **Physical** | Energy, sleep, sensory functions |
| **Level of Independence** | Mobility, daily activities, dependence on aids |
| **Social Relationships** | Personal support, community participation |
| **Environment** | Safety/security, home environment, healthcare access, transport, pollution/noise, recreation, financial resources |
| **Spirituality/Personal Beliefs** | Overall perceived QoL and general health |

#### Layer 2 — Urban QoL (QOUL) 4-Domain Operational Framework
Derived from indicators literature; the working operational framework for this dashboard:

1. **Socio-economic security** — employment stability, perceived safety, crime statistics, social capital
2. **Mobility** — commute time (10–90 min WBCSD scale), public transport affordability, traffic safety, accessibility for reduced mobility, intermodality, CO₂ reduction
3. **Accessibility** — spatial proximity to healthcare/education/recreation, spatial equity across neighborhoods, perceived safety in public spaces
4. **Environmental health** — PM2.5/PM10, NO₂, O₃, noise, urban heat island effect, green space proximity and quality

#### Layer 3 — 15-Minute City (Moreno et al., 2021)
Six social functions: **Live, Work, Shop, Healthcare, School, Fun**
Four enabling dimensions: **Density, Proximity, Diversity, Digitalization**
Key caveat: a 15-min walk for a young adult is ~25 min for an elderly person → "soft mobility" must factor in.

#### Layer 4 — Healthy Built Environment (PHSA 2014)
Five physical characteristics: Complete/Compact/Connected neighborhoods, Healthy Transport Networks, Natural Environments, Housing, Food Systems.

### Key Conceptual Distinctions

| Distinction | Description | Dashboard Implication |
|---|---|---|
| **Objective vs. Subjective QoL** | Objective = measurable physical features; Subjective = individual perception. Neither alone is sufficient. | Dashboard shows objective data; theory page explains the gap |
| **Individual vs. Population level** | WHOQOL = individual clinical tool; OECD/Mercer = city-level ranking | Dashboard operates at district (neighborhood) level — bridging gap |
| **Top-down vs. Bottom-up** | Top-down: happiness shapes domain perception. Bottom-up: domain experiences build life satisfaction. | Persona views = bottom-up; composite index = top-down synthesis |
| **Spatial equity** | Fair distribution of services across neighborhoods; "pockets of disadvantage" | Density normalization (per km²) reveals inequity raw counts hide |
| **Frequency vs. Intensity** (Diener) | Frequent small changes to urban environment > rare large projects | Longitudinal trend view (future) |

### Prague-Specific Contexts from Thesis
- **Jan (age 75, Holešovice, Praha 7):** barrier-free transport, Stromovka Park, Urban Heat Island vulnerability
- **Elena (age 28, Karlín):** metro + bike intermodality, walkable mixed-use, air quality
- **Novák family (Dejvice, Praha 6):** schools, pediatricians, PM2.5 near Evropská street
- **Golemio** = Prague's open urban data platform (primary future data source)

---

## 2. Current Project Audit

### Application Architecture
- **Framework:** Python Dash + dash-bootstrap-components + Plotly + GeoPandas
- **Entry point:** `src/app.py` — initializes Dash, mounts navbar, sidebar, page_container
- **Routing:** Dash Pages (`use_pages=True`), 6 registered pages
- **Caching:** Flask-Caching `SimpleCache`, 300s timeout on geospatial computations

### Pages

| Page | Path | Purpose | Limitations |
|---|---|---|---|
| **Home** | `/` | Landing page with two storytelling cards linking to dashboard + districts | Purely navigational; no QoL theory or context |
| **Dashboard** | `/dashboard` | District selector (multi) + data selector (single) → bar chart; click bar → single district map | Raw counts only (no normalization); only 9 datasets; no composite view |
| **Districts** | `/districts` | Interactive choropleth map of all Prague districts; click → detail | No data overlaid on overview map |
| **District Info** | `/districts/district-detail` | Single district map + safety section + travel section + toggleable layers | Only 2 sections (safety/travel); no environment, accessibility, or QoL scoring |
| **Datasets** | `/datasets` | Accordion list of dataset README docs | Documentation only; no analysis |
| **About** | `/about` | Placeholder — title only | Empty; no theory, methodology, or project context |

### Existing Datasets

| Dataset | Type | Key Fields | QoL Domain |
|---|---|---|---|
| `mestske_casti` | Polygon (57 districts) | nazev_1, shape_Area, geometry | (Administrative boundary) |
| `objekty_mestske_policie_praha` | Point | or_mp, nku, nvpk, pozn | Socio-economic security (Safety) |
| `parkovaci_automaty` | Point | pa, px, street, code | Mobility |
| `parkovaci_stani_ztp` | Point | pocet_ps, rozm_delka, rozm_sirka, typ_ps | Accessibility (Disabled) |
| `parkovani_p_r` | Point | nazev, kapacita, kapacita_vyhled, typ, stav | Mobility (Intermodality) |
| `useky_placeneho_stani` | Polygon | typzony, tariftab, ps_zps | Mobility |
| `vyhrazene_stani_pro_zasobovani` | Polygon | zps_id | Mobility |
| `vyhrazene_stani_specialni` | Polygon | zps_id | Mobility |
| `vstupy_do_metra` | Point | uzel_nazev, vst_linka (A/B/C), vst_vytah (elevator), vst_eskal, vst_schod | Mobility + Accessibility |
| `zakaz_stani` | Polygon | zps_id | Mobility |

### Missing Data / Limitations

- No green space / parks data (Environmental health domain)
- No air quality / noise data (Environmental health domain)
- No healthcare facility data (Accessibility domain)
- No education facility data (15-Minute City)
- No food/commerce accessibility data (15-Minute City)
- No demographic / population data (prevents per-capita normalization)
- No bike-sharing or pedestrian infrastructure data (Mobility)
- Bar chart shows raw counts only — misleading across districts of different sizes
- No composite QoL index or cross-domain scoring
- About page is empty — no explanation of methodology or theory
- Metro entrance data has barrier-free fields (`vst_vytah`, `vst_eskal`) that are unused
- P+R data has `kapacita` / `kapacita_vyhled` (planned capacity) that are unused
- ZTP parking data has detailed physical attributes (dimensions, surface type) that are unused

---

## 3. Feature Roadmap

Features are ordered by implementation priority: smallest/most impactful first, largest last.

---

### F1 — Normalized Density Toggle on Bar Chart
**Theory:** Stiglitz-Sen-Fitoussi: raw counts obscure spatial equity; QOUL "spatial equity" concept — fair distribution across neighborhoods of different sizes.
**Data needed:** Existing data + district area (derivable from geojson geometry via EPSG:5514 reprojection)
**Visualization:** Add "Raw count / Per km²" RadioItems toggle above the bar chart
**Complexity:** Small
**Status:** `[x] Done`

---

### F2 — Metro Barrier-Free Accessibility Analysis
**Theory:** WHOQOL Level of Independence domain; QOUL Mobility — "accessibility for reduced mobility"; Jan persona (age 75) — barrier-free tram/metro.
**Data needed:** `vstupy_do_metra` (existing) — fields `vst_vytah` (elevator), `vst_eskal` (escalator), `vst_schod` (stairs), `vst_linka` (metro line A/B/C)
**Visualization:** New section in District Info page + Dashboard dataset: stacked bar showing elevator/escalator/stairs-only entrances per district; accessibility ratio metric card
**Complexity:** Medium
**Status:** `[x] Done`

---

### F3 — Disabled Parking (ZTP) Density Score
**Theory:** WHOQOL Level of Independence; QOUL Accessibility; physical accessibility for mobility-impaired residents
**Data needed:** `parkovaci_stani_ztp` (existing) — `pocet_ps` (number of spaces), `typ_ps` (type)
**Visualization:** Add ZTP parking analysis section to District Info page; per-district metric card showing total spaces and density; add to dashboard dropdown with poc_ps sum (not just point count)
**Complexity:** Small
**Status:** `[x] Done`

---

### F4 — P+R Capacity and Intermodality View
**Theory:** QOUL Mobility — intermodality, WBCSD indicators; reducing car dependence through transit-parking integration
**Data needed:** `parkovani_p_r` (existing) — `kapacita` (current), `kapacita_vyhled` (planned), `nazev`, `stav`
**Visualization:** P+R capacity card on district detail; capacity utilization indicator (current vs. planned); add to dashboard with capacity sum instead of point count
**Complexity:** Small
**Status:** `[x] Done`

---

### F5 — QoL Theory Page (Objective vs. Subjective)
**Theory:** Central thesis distinction — objective indicators (infrastructure) vs. subjective well-being (perception); Marans dual-methodology; WHOQOL vs. OECD Better Life Index comparison
**Data needed:** None (content page)
**Visualization:** New page `/theory` — explains WHOQOL, QOUL 4 domains, 15-Minute City, objective vs. subjective QoL distinction using Prague data as live examples
**Complexity:** Medium
**Status:** `[x] Done`

---

### F6 — Persona-Based Dashboard View
**Theory:** Thesis scenario case studies — Jan (75, senior, Holešovice), Elena (28, tech, Karlín), Novák family (30s, Dejvice). Bottom-up approach: same objective data → different subjective relevance per persona.
**Data needed:** Existing data, filtered and weighted by persona-relevant criteria
**Visualization:** Persona selector (3 cards: Jan / Elena / Novák family) that reconfigures the district info page to highlight relevant layers, shows persona-specific metrics, and explains the QoL implications for that user type
**Complexity:** Large
**Status:** `[x] Done`

---

### F7 — QoL Composite Index and Radar Chart
**Theory:** OECD Better Life Index approach; normalization and weighting of multiple QOUL domains; spatial equity analysis; Marans top-down synthesis
**Data needed:** Computed from all existing data: safety (police density), mobility (metro + P+R), accessibility (ZTP parking + metro elevator ratio), district area
**Visualization:** Radar chart per district showing normalized scores across 4 QOUL domains; city-wide choropleth map colored by composite QoL index; ranking table of all districts
**Complexity:** Large
**Status:** `[x] Done`

---

## 4. Progress Log

_This section is updated after each implemented feature._

### 2026-06-09 — F1: Normalized Density Toggle
- Added `RadioItems` toggle ("Počet objektů" / "Hustota / km²") to dashboard layout above bar chart
- Added `get_district_areas_km2()` to `district_utils.py` — reprojects districts to EPSG:5514 for accurate m² → km² area calculation
- Updated `update_output` callback to accept normalization mode; when density mode is active, divides raw count by district area in km²; hover tooltip shows raw count + total area context
- Files changed: `src/utils/districts/district_utils.py`, `src/pages/dashboard.py`, `src/callbacks/dashboard_callbacks.py`
- Decision: rounded density to 4 decimal places (many small districts have < 1 obj/km²)
- Theory linkage: Stiglitz-Sen-Fitoussi / QOUL spatial equity — raw counts obscure inequity across districts of vastly different sizes (smallest: Petrovice 1.8 km², largest: Praha 6 41.6 km²)

### 2026-06-09 — F2: Metro Barrier-Free Accessibility Analysis
- Created `src/components/pages/district_info/accessibility_section.py` — new "Přístupnost metra" section
- Shows: total metro entrances, elevator count, stairs-only count, % barrier-free with color-coded progress bar, metro line badges (A/B/C)
- Added `ACCESSIBILITY_ACCENT_COLOR/BG_COLOR/TEXT_COLOR` to `src/components/config/theme.py`
- Integrated into district detail page layout after the travel section
- Data: Praha 1 has 56 entrances, only 10.7% with elevator — illustrates gap for the Jan (age 75) persona
- Theory linkage: WHOQOL Level of Independence domain; QOUL Mobility — "accessibility for reduced mobility"; Jan persona (Holešovice)

### 2026-06-09 — F3: Disabled Parking (ZTP) Density Score
- Extended `accessibility_section.py` to include ZTP parking subsection within the same "Přístupnost" section
- Added `_get_ztp_stats()`: counts ZTP parking locations + sums `pocet_ps` (actual spaces, not just point count) + computes density per km²
- Shows: number of parking locations, total spaces, spaces per km²
- Example: Praha 1 has 216 ZTP spaces (39/km²), Praha 6 has 296 spaces (7.1/km²) — density map reveals equity differences
- Theory linkage: WHOQOL Level of Independence; QOUL Accessibility — physical accessibility for mobility-impaired residents; demonstrates spatial equity concept (Stiglitz-Sen-Fitoussi)

### 2026-06-09 — F4: P+R Capacity and Intermodality View
- Created `src/components/pages/district_info/pr_section.py` — "Intermodalita (P+R)" section
- Shows: P+R count, current total capacity, planned future capacity, individual facility table (name, spaces, status)
- Section renders only for districts that contain P+R (most inner districts return None)
- Example: Praha 10 has 4 P+R facilities, 474 current spaces + 690 planned (expansion insight)
- Theory linkage: QOUL Mobility — intermodality; WBCSD mobility indicator on seamless transit-parking transfer; reducing car-dependence for full journey

### 2026-06-09 — F5: QoL Theory Page
- Created `src/pages/theory.py` — new route `/theory` "Teoretický rámec"
- Six content sections: Objective vs. Subjective QoL, QOUL 4 domains with indicator details, 15-Minute City, WHOQOL 6 domains, Persona profiles (Jan/Elena/Novákovi), Measurement frameworks
- Each QOUL domain links to specific dashboard indicators already implemented
- The three thesis personas (Jan 75, Elena 28, Novákovi family) shown with their relevant QoL factors
- Added "Teorie" to sidebar navigation
- Theory linkage: central thesis distinction — operationalizes the entire theoretical framework as an interactive explainer that can be used while writing thesis chapters

### 2026-06-09 — F6: Persona-Based Dashboard View
- Created `src/pages/personas.py` — new route `/personas` "Persony"
- Three persona cards (Jan 75/Praha 7, Elena 28/Praha 8, Novákovi/Praha 6) selectable via URL query param `?persona=`
- Each persona shows: their QoL concerns list, live district metrics from existing data, and a personalized insight text explaining the data through their lens
- Jan: elevator ratio (only 10.7% in Praha 1), ZTP parking density, police stations
- Elena: metro line coverage, P+R intermodality, parking meter density
- Novákovi: police density, metro accessibility with pram (elevator ratio), ZTP density, air quality note (data gap)
- Quick-links to the district detail page and theory page
- Added "Persony" to sidebar navigation
- Theory linkage: Chapter 5 scenario case studies; Marans dual-methodology; Diener's bottom-up SWB approach — same objective data → different subjective implications

### 2026-06-09 — F7: QoL Composite Index and Radar Chart
- Created `src/pages/qol_index.py` — new route `/qol-index` "QoL Index"
- Scoring architecture: 4 QOUL domains, each normalized 0–100 via min-max scaling (OECD Better Life Index method)
  - Bezpečnost (30%): police station density / km²
  - Mobilita (37%): 70% metro density + 30% elevator ratio
  - Přístupnost (23%): 60% ZTP density + 40% elevator ratio
  - Prostředí (10%): park density (OSM, parks/km²) — activated in Phase 4 with parks data
- Interactive radar chart for any selected district (Dash callback)
- Domain score cards showing each QOUL domain score + composite
- Full district ranking horizontal bar chart (green/amber/red by score tier)
- Domain methodology cards explaining each indicator and data source
- Result: Praha 1 scores 80.4 composite (high metro density drives mobility); outer rural districts score near 0
- Explicit data-gap notice: Environment domain awaits Golemio air quality / green space data
- Added "QoL Index" to sidebar navigation
- Theory linkage: OECD Better Life Index approach; Stiglitz-Sen-Fitoussi normalization; Marans top-down synthesis; spatial equity visualization

---

## 5. New Datasets (Phase 3 — Discovery & Download)

_Datasets acquired 2026-06-09. Not yet integrated into application code — discovery and documentation only._

### Dataset Inventory

| Dataset | Folder | Format | Count | QoL Domain | Source |
|---|---|---|---|---|---|
| Nextbike bike-sharing stations | `nextbike_stanice/` | GeoJSON (Point) | 217 stations | Mobility | GBFS v2.3 open feed |
| PID public transport stops | `zastavky_pid/` | GeoJSON (Point) | 3,609 stop platforms | Mobility | data.pid.cz |
| ČHMÚ air quality monitoring stations | `stanice_kvality_ovzdusi/` | GeoJSON (Point) | 14 Prague stations | Environmental Health | opendata.chmi.cz |
| ČSÚ district demographics time series | `demograficke_udaje_mc/` | XLSX (22 sheets, 2004–2025) | 57 districts × 22 years | Socio-economic Security | ČSÚ / csu.gov.cz |
| Parks and green spaces (OSM) | `parky_praha/` | GeoJSON (Point centroids) | 1,054 parks | Environmental Health | OpenStreetMap / Overpass API |

### Dataset Details

#### Nextbike Stanice (`nextbike_stanice/`)
- **Source:** Nextbike GBFS v2.3 live feed (station_information.json)
- **Key fields:** `station_id`, `name` (P{district}-{location}), `capacity`, `region_id`
- **Integration potential:** Bike-sharing density per district; combined mobility score with metro + P+R; intermodal analysis (bike station proximity to metro entrances)
- **QoL mapping:** QOUL Mobility — cycling as sustainable last-mile transport; 15-Minute City "Diversity" dimension; Elena persona (Karlín bike commuter)

#### Zastávky PID (`zastavky_pid/`)
- **Source:** Ropid open data (18 MB JSON, converted to GeoJSON)
- **Key fields:** `stop_id`, `stop_name`, `zone`, `traffic_type` (metro/tram/bus/train/ferry), `wheelchair`
- **Integration potential:** Public transport coverage score per district (stops/km²); modal breakdown (tram vs. bus dominance); wheelchair-accessible stop ratio; 15-Minute City proximity scoring
- **QoL mapping:** QOUL Mobility domain — PT coverage and multimodality; WHOQOL Level of Independence — wheelchair access for Jan persona

#### Stanice Kvality Ovzduší (`stanice_kvality_ovzdusi/`)
- **Source:** ČHMÚ OpenData metadata.json (all 98 CZ stations, filtered to 14 Prague)
- **Key fields:** `station_code`, `name`, `station_type` (background/traffic/industrial), `zone_type`
- **Integration potential:** District-level PM2.5/PM10/NO₂ data via per-station measurement feeds at `https://opendata.chmi.cz/air_quality/recent/{station_code}/`; air quality score per district by nearest station interpolation
- **QoL mapping:** QOUL Environmental Health — PM2.5, NO₂ exposure; Novák family persona (Dejvice/Evropská); unlocks Environment domain in QoL Index (currently 0% placeholder)

#### Demografické Údaje MC (`demograficke_udaje_mc/`)
- **Source:** ČSÚ time series XLSX (last updated 2026-04-13)
- **Key fields:** Population, age groups (0–14, 15–64, 65+), mean age, birth/death rates, population density, area (ha)
- **Integration potential:**
  - Per-capita normalization: police/km² → police/1000 residents (more meaningful)
  - Elderly population (65+) per district → priority map for barrier-free infrastructure demand
  - Population density as urbanization proxy for the Environment domain
  - Longitudinal trend view (2004–2025) — population growth/decline per district
- **QoL mapping:** QOUL Socio-economic Security; OECD Better Life Index denominator; Stiglitz-Sen-Fitoussi per-capita normalization

#### Parky Praha (`parky_praha/`)
- **Source:** OpenStreetMap via Overpass API (bbox query, `leisure=park`)
- **Key fields:** `osm_id`, `name`, `access`, `operator`, `wikipedia`
- **Integration potential:** Park count and density per district; nearest park proximity (walkability score); green space coverage as QoL Index Environment domain input; 15-Minute City "Fun" function coverage map
- **QoL mapping:** QOUL Environmental Health — green space access; WHOQOL Physical domain; 15-Minute City recreational accessibility; urban heat island mitigation proxy

### Datasets Not Yet Acquired

| Dataset | Source | Reason Not Downloaded | Priority |
|---|---|---|---|
| NRPZS healthcare facilities | opendata.uzis.cz (28 MB CSV) | Server not responding at download time | High — unlocks Accessibility domain healthcare component |
| ČHMÚ hourly air quality measurements | opendata.chmi.cz/air_quality/recent/{code}/ | Per-station files, requires multi-step aggregation | High — unlocks Environment domain in QoL Index |
| Prague green space polygons (area) | Geoportál Praha / IPR Praha | GeoPortal serves JS-rendered pages; ArcGIS Hub restricted | Medium — would improve on OSM centroid-only approach |
| Prague cycling infrastructure | Geoportál Praha WFS | Not accessible from automated requests | Medium — QOUL Mobility cycling dimension |
| School locations (ZŠ, MŠ) | Geoportál Praha / MŠMT | Dataset UUID not found in accessible catalog | Medium — 15-Minute City "School" function |
| Noise pollution map | IPR Praha / Zákon o hluku | No open-data GeoJSON endpoint found | Medium — Environmental Health domain |

### Next Integration Steps (Phase 4 — not yet started)
1. **Unlock Environment domain in QoL Index** — integrate ČHMÚ air quality data (download per-station hourly CSV, compute 30-day PM2.5 mean, map to district via nearest-station interpolation)
2. **Add per-capita normalization** — use ČSÚ population data to normalize safety/mobility/accessibility scores by district population (e.g., police stations per 1000 residents vs. per km²)
3. **Expand Dashboard dropdown** — add PID stop density, bike station density, and park count as selectable metrics
4. **Park proximity layer** — add nearest park distance as a district metric (requires point-to-polygon distance calculation using district centroids)
5. **Elderly population vulnerability map** — combine 65+ population share with barrier-free metro ratio and ZTP density to identify districts most at risk for Jan persona

---

## 6. Dataset Integration Log (Phase 4 — Completed 2026-06-09)

_All 5 Phase 3 datasets integrated into application code. No existing functionality was removed or broken._

### Integration Status per Dataset

| Dataset | Status | Placed In | Visualization Used |
|---|---|---|---|
| `parky_praha/` (OSM parks) | **Done** | District Info → Environment section; QoL Index → Prostředí domain | Count + density stat cards; park density drives 10% weight in composite QoL score |
| `nextbike_stanice/` (Nextbike) | **Done** | District Info → Mobility section | Station count + total capacity + avg capacity/station stat cards |
| `zastavky_pid/` (PID stops) | **Done** | District Info → Mobility section | Total stops + density + wheelchair count stat cards; mode badges (Metro A/B/C, tram, bus); wheelchair ratio badge |
| `stanice_kvality_ovzdusi/` (ČHMÚ) | **Done (partial)** | District Info → Environment section (nearest station metadata) | Station info card (name, code, type, distance); measurement data deferred to Phase 5 |
| `demograficke_udaje_mc/` (ČSÚ demographics) | **Done** | District Info → Demographics section (new) | Population + density + mean age + 65% share stat cards; stacked horizontal age distribution bar |

### Per-Dataset Integration Notes

#### Parks (`parky_praha/`) — Done
- **New files:** `environment_section.py` (handles both parks + ČHMÚ)
- **QoL Index change:** `park_density` (parks/km²) now drives the "Prostředí" domain (was placeholder 0); weight set to 10% to reflect partial coverage (parks only, no air quality yet)
- **Decision:** OSM centroids used (not polygon areas) — parks stored as Point features after Overpass API download. This counts distinct park features accurately but does not measure green area in m²
- **Tradeoff:** Environment domain remains partial (10% weight); full activation awaits ČHMÚ measurement API integration

#### Nextbike (`nextbike_stanice/`) — Done
- **New section:** `_get_nextbike_stats()` inside `mobility_section.py` — placed in same section as PID stops for coherent Mobility grouping
- **Decision:** `section="mobility"` in DATASET_CONFIGS (not "travel") so the dataset does not auto-appear in the existing `travel_section.py` loop, avoiding unplanned modifications to working code
- **Tradeoff:** Not yet added to the Dashboard bar chart dropdown — only visible on District Info page

#### PID Stops (`zastavky_pid/`) — Done
- **New section:** `_get_pid_stats()` inside `mobility_section.py`
- **Bug found and fixed during integration:** `traffic_type` in the GeoJSON uses `'metroA'`, `'metroB'`, `'metroC'` (separate per-line values), not a single `'metro'` value. Initial `_TRAFFIC_LABELS` dict only mapped `'metro'`; all metro stops were silently omitted. Fixed by adding all three variants.
- **Decision:** `'undefined'` traffic type hidden from mode badges to keep UI clean — it is captured in the total count but not labelled
- **Tradeoff:** Not yet added to the Dashboard dropdown

#### ČHMÚ Stations (`stanice_kvality_ovzdusi/`) — Done (partial)
- **Placed in:** `environment_section.py` — shows nearest station metadata per district
- **Geospatial approach:** Projects to EPSG:5514 for accurate km distance calculation, finds nearest station to district centroid
- **Decision:** Shows station name, code, type (background/traffic/industrial), and whether it's within the district. Actual PM2.5/PM10/NO₂ measurements not integrated — measurement API requires separate per-station CSV download and aggregation (deferred)
- **Tradeoff:** ČHMÚ section informs users which station monitors their district but does not yet show live or historical pollution readings

#### ČSÚ Demographics (`demograficke_udaje_mc/`) — Done
- **New files:** `src/utils/loaders/xlsx_loader.py`, `src/components/pages/district_info/demographics_section.py`
- **XLSX parsing approach:** openpyxl + importlib.resources; sheet per year (2004–2025); districts as columns; indicators as rows matched via partial string patterns
- **Bug found and fixed during integration:** Row 132 in the XLSX ("dosažitelní uchazeči ženy ve věku 15 - 64") matched the `"15 - 64"` age percentage pattern and was overwriting the correct row 19 value. Fixed with `setdefault()` (first-occurrence-wins strategy)
- **Bug found and fixed:** District names in XLSX use "Praha-Kunratice" prefix while GeoJSON uses "Kunratice". Fixed via `_normalise_district()` helper that strips the "Praha-" prefix
- **Decision:** Year 2024 hardcoded in section call; `@lru_cache` on the loader supports future year-selector without refactoring
- **Tradeoff:** Demographics data not yet used for per-capita normalization in QoL Index (police/1000 residents vs. police/km²) — deferred to Phase 5

### New Files Created

| File | Purpose |
|---|---|
| `src/components/pages/district_info/environment_section.py` | Parks + ČHMÚ section for District Info |
| `src/components/pages/district_info/demographics_section.py` | ČSÚ demographics section for District Info |
| `src/components/pages/district_info/mobility_section.py` | PID stops + Nextbike section for District Info |
| `src/utils/loaders/xlsx_loader.py` | XLSX parser for ČSÚ demographics with district name normalization |

### Existing Files Modified

| File | What Changed | Why |
|---|---|---|
| `src/configs/data_config.py` | Added `parks`, `nextbike`, `pid_stops`, `chmi_stations` path fields; added 3 entries to `label_map` | Required to expose new datasets through the existing data loader pattern |
| `src/utils/loaders/districts_loader.py` | Added 4 new loader functions | Consistent with existing pattern; used by both section components and QoL Index |
| `src/configs/dataset_config.py` | Added 3 new DATASET_CONFIGS entries | Required for dashboard bar chart dataset dropdown (parks, nextbike, pid_stops) |
| `src/utils/scatter/scatter_configs.py` | Added 3 scatter layer configs | Required for map layer rendering in district detail |
| `src/components/config/theme.py` | Added 9 color constants for 3 new sections | Consistent theming for environment/mobility/demographics sections |
| `src/pages/qol_index.py` | Added park density to `_compute_raw_scores()`; activated Prostředí domain with `park_norm`; updated weights (S 30%, M 37%, A 23%, E 10%); updated UI text | Environment domain was a 0% placeholder; now driven by real park data |
| `src/pages/district_info.py` | Added 3 new section imports + 3 new section mounts | Required to render the new sections in the district detail layout |

### Remaining Gaps (Phase 5 Candidates)

- ČHMÚ measurement data (PM2.5/PM10/NO₂): will activate air quality score in Environment domain; raises Prostředí weight from 10% to ~20%
- Per-capita normalization (police/1000 residents, metro density per 1000 residents): requires ČSÚ population denominator now available in `xlsx_loader.py`
- PID stops + Nextbike in Dashboard bar chart dropdown: data is loaded and available; just needs entries in `label_map` and `DATASET_CONFIGS`
- NRPZS healthcare facilities: server was unresponsive at download time; high-priority for Accessibility domain