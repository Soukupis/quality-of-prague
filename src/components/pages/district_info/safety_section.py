"""Safety metrics section for district detail pages.

Operationalises the QOUL Socio-economic Security domain by showing:
  - Municipal police station count, spatial density, and comparison to
    the Prague city average
  - Station type breakdown (regular patrol stations vs. district HQ)
  - Annotated list of all police facilities in the district
  - Toggleable map layer for police station locations

Theory reference: QOUL Socio-economic Security — perceived safety, police
presence as infrastructure proxy; Stiglitz-Sen-Fitoussi subjective safety
perception; WHOQOL Environment domain — safety/security facet.
"""
from dash import html
import dash_bootstrap_components as dbc

from src.components.ui import info_card, section_header
from src.configs.dataset_config import DATASET_CONFIGS
from src.utils.geospatial_utils import point_count_for_polygon, points_within_polygon
from src.utils.loaders.districts_loader import get_police_stations_data
from src.utils.districts.district_utils import get_district_areas_km2
from src.components.config import theme


def _stat_card(icon_class, label, value, color="#b45309"):
    """Compact read-only stat card matching the section visual style."""
    return dbc.Card(
        dbc.CardBody(
            html.Div([
                html.I(className=f"fa-solid {icon_class}",
                       style={"fontSize": "1.3rem", "color": color, "minWidth": "1.6rem"}),
                html.Div([
                    html.Div(label, style={"fontSize": "0.8rem", "color": "#64748b",
                                           "fontWeight": "500", "lineHeight": "1.2"}),
                    html.Div(str(value), style={"fontSize": "1.3rem", "fontWeight": "700",
                                                "color": "#1e293b", "lineHeight": "1.3"}),
                ], style={"marginLeft": "0.5rem"})
            ], className="d-flex align-items-center"),
        ),
        className="shadow-sm h-100",
        style={"border": "none", "borderRadius": "0.75rem",
               "background": "linear-gradient(135deg, #fffbf5 0%, #ffffff 100%)"}
    )


def _density_badge(district_density, city_density):
    """Colored badge comparing district police density to city average."""
    if city_density == 0:
        return None
    ratio = district_density / city_density
    if ratio >= 1.5:
        color, text = "#059669", f"↑ {ratio:.1f}× průměr Prahy"
    elif ratio >= 0.5:
        color, text = "#d97706", "≈ průměr Prahy"
    else:
        color, text = "#dc2626", f"↓ pod průměrem Prahy"
    return html.Span(
        text,
        style={
            "display": "inline-block", "background": color, "color": "white",
            "borderRadius": "12px", "padding": "2px 10px",
            "fontSize": "0.82rem", "fontWeight": "600",
            "marginLeft": "0.5rem", "verticalAlign": "middle",
        }
    )


def _get_safety_stats(district, district_polygon):
    """Compute police station statistics for a district.

    Args:
        district: District name string (for area lookup).
        district_polygon: Shapely polygon for the district boundary.

    Returns:
        dict with keys: count, density, city_density,
        regular, hq, special, stations (list of dicts).
    """
    data = get_police_stations_data()
    within = points_within_polygon(district_polygon, data, "geometry")
    count = len(within)

    areas = get_district_areas_km2()
    area_km2 = areas.get(district, 1.0)
    density = round(count / area_km2, 3) if area_km2 > 0 else 0.0

    city_total_area = sum(areas.values())
    city_density = round(len(data) / city_total_area, 3)

    regular = hq = special = 0
    stations = []
    if count > 0:
        for _, row in within.iterrows():
            pozn = str(row.get("pozn", ""))
            nvpk = str(row.get("nvpk", ""))
            if "Služebna" in pozn:
                regular += 1
                cat = "Služebna"
            elif "OŘ MP" in pozn:
                hq += 1
                cat = "Řídící oddělení"
            else:
                special += 1
                cat = "Speciální útvar"
            stations.append({"address": nvpk, "type": pozn, "category": cat})

    return {
        "count": count,
        "density": density,
        "city_density": city_density,
        "regular": regular,
        "hq": hq,
        "special": special,
        "stations": stations,
    }


_STATION_CATEGORY_STYLES = {
    "Služebna":          ("#fef3c7", "#92400e"),
    "Řídící oddělení":   ("#fce7f3", "#9d174d"),
    "Speciální útvar":   ("#ede9fe", "#5b21b6"),
}

_TYPE_BADGE_COLORS = {
    "Služebna":          "#b45309",
    "Řídící oddělení":   "#9d174d",
    "Speciální útvar":   "#5b21b6",
}


def _station_row(station):
    """Render one police facility as a compact table row."""
    bg, fg = _STATION_CATEGORY_STYLES.get(station["category"], ("#f1f5f9", "#334155"))
    return html.Tr([
        html.Td(
            html.I(className="fa-solid fa-building-shield",
                   style={"color": "#b45309", "fontSize": "0.9rem"}),
            style={"paddingRight": "0.75rem", "paddingBottom": "0.5rem",
                   "verticalAlign": "middle"}
        ),
        html.Td(
            station["address"],
            style={"fontSize": "0.85rem", "fontWeight": "500", "color": "#1e293b",
                   "paddingRight": "1rem", "paddingBottom": "0.5rem"}
        ),
        html.Td(
            html.Span(
                station["category"],
                style={"fontSize": "0.75rem", "background": bg, "color": fg,
                       "borderRadius": "8px", "padding": "2px 8px", "fontWeight": "600"}
            ),
            style={"paddingBottom": "0.5rem", "whiteSpace": "nowrap"}
        ),
    ], style={"borderBottom": "1px solid #f1f5f9"})


def safety_section(district, polygons):
    """Create the safety metrics section for a district detail page.

    Shows police station counts, density comparison to the Prague average,
    station type breakdown, and a facility list. Also renders a toggleable
    map layer card for police station locations.

    Args:
        district: Name of the district (e.g., "Praha 1").
        polygons: Dictionary mapping district names to their Shapely polygon
            geometries.

    Returns:
        dbc.Row with the safety section, or None if no safety datasets are
        configured.
    """
    police_stations = get_police_stations_data()

    cards = []
    for dataset_key, config in DATASET_CONFIGS.items():
        if config.get("section") == "safety":
            if dataset_key == "police_stations":
                count = point_count_for_polygon(polygons[district], police_stations, "geometry")
                cards.append(
                    info_card(
                        config["icon"],
                        config["title"],
                        count,
                        "info",
                        card_id=config["id"],
                        dataset_key=dataset_key,
                        compact=True,
                        color=config.get("color", "#334155"),
                    )
                )

    if not cards:
        return None

    stats = _get_safety_stats(district, polygons[district])

    # --- Stats subsection ---
    stats_content = [
        html.H6("Obecní policie — pokrytí obvodu",
                style={"color": theme.SAFETY_TEXT_COLOR, "fontWeight": "600",
                       "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
        dbc.Row([
            dbc.Col(_stat_card("fa-building-shield", "Stanic celkem",
                               stats["count"], "#b45309"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_stat_card("fa-map", "Stanic / km²",
                               f"{stats['density']:.3f}", "#92400e"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_stat_card("fa-city", "Průměr Prahy / km²",
                               f"{stats['city_density']:.3f}", "#78350f"),
                    xs=6, sm=4, md=3, className="mb-3"),
        ], className="g-2 mb-2"),
    ]

    # Density comparison badge
    stats_content.append(
        html.Div([
            html.Span("Hustota pokrytí:",
                      style={"fontSize": "0.85rem", "color": "#475569", "fontWeight": "500"}),
            _density_badge(stats["density"], stats["city_density"]),
        ], className="d-flex align-items-center mb-3")
    )

    # Station type breakdown badges
    if stats["count"] > 1:
        type_badges = []
        for label, key in [("Služebna", "regular"),
                            ("Řídící oddělení", "hq"),
                            ("Speciální útvar", "special")]:
            n = stats[key]
            if n > 0:
                type_badges.append(html.Span(
                    f"{label}: {n}",
                    style={
                        "display": "inline-block",
                        "background": _TYPE_BADGE_COLORS[label],
                        "color": "white",
                        "borderRadius": "8px", "padding": "3px 10px",
                        "fontSize": "0.82rem", "fontWeight": "700",
                        "marginRight": "0.4rem", "marginBottom": "0.3rem",
                    }
                ))
        if type_badges:
            stats_content.append(
                html.Div([
                    html.Span("Druhy objektů: ",
                              style={"fontSize": "0.85rem", "color": "#475569",
                                     "fontWeight": "500", "marginRight": "0.3rem"}),
                    *type_badges,
                ], className="d-flex flex-wrap align-items-center mb-3")
            )
    elif stats["count"] == 0:
        stats_content.append(
            html.Div([
                html.I(className="fa-solid fa-building-shield me-2",
                       style={"color": "#94a3b8"}),
                html.Span("V tomto obvodu nejsou evidovány žádné objekty Obecní policie Praha.",
                          style={"fontSize": "0.82rem", "color": "#94a3b8"}),
            ], className="mb-3")
        )

    # --- Station list table (only when there are ≤ 15 facilities) ---
    station_table_content = []
    if 0 < stats["count"] <= 15:
        station_table_content = [
            html.H6("Přehled objektů",
                    style={"color": theme.SAFETY_TEXT_COLOR, "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
            html.Div(
                html.Table(
                    [html.Tbody([_station_row(s) for s in stats["stations"]])],
                    style={"width": "100%", "borderCollapse": "collapse"}
                ),
                style={"background": "#f8fafc", "borderRadius": "0.75rem",
                       "padding": "0.75rem 1rem", "marginBottom": "0.75rem"}
            ),
        ]

    return dbc.Row([
        dbc.Col([
            section_header(
                title="Bezpečnost",
                accent_color=theme.SAFETY_ACCENT_COLOR,
                bg_color=theme.SAFETY_BG_COLOR,
                text_color=theme.SAFETY_TEXT_COLOR
            ),
            *stats_content,
            *station_table_content,
            html.H6("Zobrazit vrstvy na mapě",
                    style={"color": theme.SAFETY_TEXT_COLOR, "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem",
                           "marginTop": "0.25rem"}),
            dbc.Row([dbc.Col(card, xs=6, sm=4, md=3, className="mb-3") for card in cards],
                    className="g-2 mb-2"),
        ], width=12)
    ])
