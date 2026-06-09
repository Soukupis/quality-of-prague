"""Travel and transportation metrics section for district detail pages.

Operationalises the QOUL Mobility domain by showing:
  - Parking meter count and density vs. Prague city average
  - Paid parking capacity (total spaces, density) and zone-type breakdown
  - Toggleable map layers for all transport-related datasets

Theory reference: QOUL Mobility — commute time, traffic safety, parking
pressure as proxy for car-mode dependency; Stiglitz-Sen-Fitoussi spatial
equity — parking provision differs dramatically across inner and outer
districts; Elena persona (Praha 8) — intermodal mobility.
"""
from dash import html
import dash_bootstrap_components as dbc

from src.components.ui import info_card, section_header
from src.configs.dataset_config import DATASET_CONFIGS
from src.utils.geospatial_utils import point_count_for_polygon, points_within_polygon
from src.utils.loaders.districts_loader import (
    get_parking_meters_data, get_subway_entrances_data,
    get_parking_p_r_data, get_no_standing_data, get_loading_zone_data,
    get_designated_parking_data, get_paid_parking_data, get_ztp_parking_data,
)
from src.utils.districts.district_utils import get_district_areas_km2
from src.components.config import theme


_ZONE_TYPE_LABELS = {
    "1": "Rezidentní (fialová)",
    "2": "Placená (oranžová)",
    "3": "Dlouhodobá",
    "7": "Zvláštní",
}

_ZONE_TYPE_COLORS = {
    "1": "#7c3aed",
    "2": "#d97706",
    "3": "#059669",
    "7": "#64748b",
}


def _stat_card(icon_class, label, value, color="#1d4ed8"):
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
               "background": "linear-gradient(135deg, #f6fffd 0%, #ffffff 100%)"}
    )


def _comparison_badge(district_val, city_val):
    """Colored badge comparing district parking density to city average."""
    if city_val == 0:
        return None
    ratio = district_val / city_val
    if ratio >= 2.0:
        color, text = "#1d4ed8", f"↑ {ratio:.1f}× průměr Prahy"
    elif ratio >= 0.5:
        color, text = "#0f766e", "≈ průměr Prahy"
    else:
        color, text = "#94a3b8", f"↓ pod průměrem Prahy"
    return html.Span(
        text,
        style={
            "display": "inline-block", "background": color, "color": "white",
            "borderRadius": "12px", "padding": "2px 10px",
            "fontSize": "0.82rem", "fontWeight": "600",
            "marginLeft": "0.5rem", "verticalAlign": "middle",
        }
    )


def _get_parking_stats(district, district_polygon):
    """Compute parking statistics for a district.

    Covers parking meters (point data) and paid parking zones (polygon data).

    Args:
        district: District name string (for area lookup).
        district_polygon: Shapely polygon for the district boundary.

    Returns:
        dict with keys: meter_count, meter_density, city_meter_density,
        paid_spaces, paid_density, city_paid_density, zone_types (dict).
    """
    areas = get_district_areas_km2()
    area_km2 = areas.get(district, 1.0)
    city_total_area = sum(areas.values())

    # Parking meters (point data)
    meters = get_parking_meters_data()
    meter_count = len(points_within_polygon(district_polygon, meters, "geometry"))
    meter_density = round(meter_count / area_km2, 1)
    city_meter_density = round(len(meters) / city_total_area, 1)

    # Paid parking zones (polygon data — use intersects for polygon features)
    paid = get_paid_parking_data()
    mask = paid["geometry"].apply(district_polygon.intersects)
    within_paid = paid[mask]
    paid_spaces = int(within_paid["ps_zps"].astype(int).sum()) if len(within_paid) > 0 else 0
    paid_density = round(paid_spaces / area_km2, 0) if area_km2 > 0 else 0.0
    city_paid_total = int(paid["ps_zps"].astype(int).sum())
    city_paid_density = round(city_paid_total / city_total_area, 0)

    # Zone type breakdown
    zone_types = {}
    if len(within_paid) > 0:
        for t in _ZONE_TYPE_LABELS:
            n = int((within_paid["typzony"].astype(str) == t).sum())
            if n > 0:
                zone_types[t] = n

    return {
        "meter_count": meter_count,
        "meter_density": meter_density,
        "city_meter_density": city_meter_density,
        "paid_spaces": paid_spaces,
        "paid_density": int(paid_density),
        "city_paid_density": int(city_paid_density),
        "zone_types": zone_types,
    }


def travel_section(district, polygons):
    """Create the transportation metrics section for a district detail page.

    Shows parking meter count/density, paid parking capacity with zone-type
    breakdown, and city-average comparisons. Also renders toggleable map
    layer cards for all transport-related datasets.

    Args:
        district: Name of the district (e.g., "Praha 1").
        polygons: Dictionary mapping district names to their Shapely polygon
            geometries.

    Returns:
        dbc.Row with the transportation section, or None if no travel datasets
        are configured.
    """
    df = {
        "parking_meters": get_parking_meters_data(),
        "subway_entrances": get_subway_entrances_data(),
        "parking_p_r": get_parking_p_r_data(),
        "no_standing": get_no_standing_data(),
        "loading_zone": get_loading_zone_data(),
        "designated_parking": get_designated_parking_data(),
        "paid_parking": get_paid_parking_data(),
        "ztp_parking": get_ztp_parking_data(),
    }

    cards = []
    for dataset_key, config in DATASET_CONFIGS.items():
        if config.get("section") == "travel":
            data = df[dataset_key]
            count = point_count_for_polygon(polygons[district], data, "geometry")
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

    stats = _get_parking_stats(district, polygons[district])

    # --- Stats subsection ---
    parking_stats_content = [
        html.H6("Parkování — statistický přehled",
                style={"color": theme.TRAVEL_TEXT_COLOR, "fontWeight": "600",
                       "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
        dbc.Row([
            dbc.Col(_stat_card("fa-parking", "Parkovacích automatů",
                               stats["meter_count"], "#1d4ed8"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_stat_card("fa-map", "Automatů / km²",
                               f"{stats['meter_density']:.1f}", "#1e40af"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_stat_card("fa-square-parking", "Placených parkovišť",
                               f"{stats['paid_spaces']:,}".replace(",", " "),
                               "#d97706"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_stat_card("fa-chart-simple", "Placených míst / km²",
                               f"{stats['paid_density']:,}".replace(",", " "),
                               "#b45309"),
                    xs=6, sm=4, md=3, className="mb-3"),
        ], className="g-2 mb-2"),
    ]

    # City comparison badge for paid parking density
    if stats["city_paid_density"] > 0:
        parking_stats_content.append(
            html.Div([
                html.Span("Hustota placených míst:",
                          style={"fontSize": "0.85rem", "color": "#475569", "fontWeight": "500"}),
                _comparison_badge(stats["paid_density"], stats["city_paid_density"]),
                html.Span(f" (průměr: {stats['city_paid_density']:,} míst/km²)".replace(",", " "),
                          style={"fontSize": "0.82rem", "color": "#94a3b8", "marginLeft": "0.4rem"}),
            ], className="d-flex align-items-center flex-wrap mb-2")
        )

    # Zone type breakdown badges
    if stats["zone_types"]:
        zone_badges = [
            html.Span(
                f"{_ZONE_TYPE_LABELS.get(t, t)}: {n}",
                style={
                    "display": "inline-block",
                    "background": _ZONE_TYPE_COLORS.get(t, "#64748b"),
                    "color": "white",
                    "borderRadius": "8px", "padding": "3px 10px",
                    "fontSize": "0.82rem", "fontWeight": "700",
                    "marginRight": "0.4rem", "marginBottom": "0.3rem",
                }
            )
            for t, n in stats["zone_types"].items()
        ]
        parking_stats_content.append(
            html.Div([
                html.Span("Typy zón placeného stání: ",
                          style={"fontSize": "0.85rem", "color": "#475569",
                                 "fontWeight": "500", "marginRight": "0.3rem"}),
                *zone_badges,
            ], className="d-flex flex-wrap align-items-center mb-3")
        )
    else:
        parking_stats_content.append(
            html.Div([
                html.I(className="fa-solid fa-coins me-2", style={"color": "#94a3b8"}),
                html.Span("V tomto obvodu nejsou evidovány žádné zóny placeného stání.",
                          style={"fontSize": "0.82rem", "color": "#94a3b8"}),
            ], className="mb-3")
        )

    return dbc.Row([
        dbc.Col([
            section_header(
                title="Doprava",
                accent_color=theme.TRAVEL_ACCENT_COLOR,
                bg_color=theme.TRAVEL_BG_COLOR,
                text_color=theme.TRAVEL_TEXT_COLOR
            ),
            *parking_stats_content,
            html.H6("Zobrazit vrstvy na mapě",
                    style={"color": theme.TRAVEL_TEXT_COLOR, "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem",
                           "marginTop": "0.25rem"}),
            dbc.Row([dbc.Col(card, xs=6, sm=4, md=3, className="mb-3") for card in cards],
                    className="g-2 mb-2"),
        ], width=12)
    ])
