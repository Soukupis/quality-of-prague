"""Travel and transportation metrics section for district detail pages."""
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
from src.i18n import t


_ZONE_TYPE_KEYS = {"1": "zone_1", "2": "zone_2", "3": "zone_3", "7": "zone_7"}
_ZONE_TYPE_COLORS = {"1": "#7c3aed", "2": "#d97706", "3": "#059669", "7": "#64748b"}


def _stat_card(icon_class, label, value, color="#1d4ed8"):
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
                ], style={"marginLeft": "0.5rem"}),
            ], className="d-flex align-items-center"),
        ),
        className="shadow-sm h-100",
        style={"border": "none", "borderRadius": "0.75rem",
               "background": "linear-gradient(135deg, #f6fffd 0%, #ffffff 100%)"},
    )


def _comparison_badge(district_val, city_val, lang):
    if city_val == 0:
        return None
    ratio = district_val / city_val
    if ratio >= 2.0:
        color, text = "#1d4ed8", t("density_above", lang, ratio=ratio)
    elif ratio >= 0.5:
        color, text = "#0f766e", t("density_near", lang)
    else:
        color, text = "#94a3b8", t("density_below", lang)
    return html.Span(
        text,
        style={
            "display": "inline-block", "background": color, "color": "white",
            "borderRadius": "12px", "padding": "2px 10px",
            "fontSize": "0.82rem", "fontWeight": "600",
            "marginLeft": "0.5rem", "verticalAlign": "middle",
        },
    )


def _get_parking_stats(district, district_polygon):
    areas = get_district_areas_km2()
    area_km2 = areas.get(district, 1.0)
    city_total_area = sum(areas.values())

    meters = get_parking_meters_data()
    meter_count = len(points_within_polygon(district_polygon, meters, "geometry"))
    meter_density = round(meter_count / area_km2, 1)
    city_meter_density = round(len(meters) / city_total_area, 1)

    paid = get_paid_parking_data()
    mask = paid["geometry"].apply(district_polygon.intersects)
    within_paid = paid[mask]
    paid_spaces = int(within_paid["ps_zps"].astype(int).sum()) if len(within_paid) > 0 else 0
    paid_density = round(paid_spaces / area_km2, 0) if area_km2 > 0 else 0.0
    city_paid_total = int(paid["ps_zps"].astype(int).sum())
    city_paid_density = round(city_paid_total / city_total_area, 0)

    zone_types = {}
    if len(within_paid) > 0:
        for zt in _ZONE_TYPE_KEYS:
            n = int((within_paid["typzony"].astype(str) == zt).sum())
            if n > 0:
                zone_types[zt] = n

    return {
        "meter_count": meter_count, "meter_density": meter_density,
        "city_meter_density": city_meter_density,
        "paid_spaces": paid_spaces, "paid_density": int(paid_density),
        "city_paid_density": int(city_paid_density), "zone_types": zone_types,
    }


def travel_section(district, polygons, lang="cs"):
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
            count = point_count_for_polygon(polygons[district], df[dataset_key], "geometry")
            cards.append(info_card(
                config["icon"], config["title"], count, "info",
                card_id=config["id"], dataset_key=dataset_key,
                compact=True, color=config.get("color", "#334155"),
            ))

    if not cards:
        return None

    stats = _get_parking_stats(district, polygons[district])

    parking_stats_content = [
        html.H6(t("travel_stats_title", lang),
                style={"color": theme.TRAVEL_TEXT_COLOR, "fontWeight": "600",
                       "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
        dbc.Row([
            dbc.Col(_stat_card("fa-parking", t("travel_meters_count", lang),
                               stats["meter_count"], "#1d4ed8"), xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_stat_card("fa-map", t("travel_meters_density", lang),
                               f"{stats['meter_density']:.1f}", "#1e40af"), xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_stat_card("fa-square-parking", t("travel_paid_spaces", lang),
                               f"{stats['paid_spaces']:,}".replace(",", " "), "#d97706"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_stat_card("fa-chart-simple", t("travel_paid_density", lang),
                               f"{stats['paid_density']:,}".replace(",", " "), "#b45309"),
                    xs=6, sm=4, md=3, className="mb-3"),
        ], className="g-2 mb-2"),
    ]

    if stats["city_paid_density"] > 0:
        parking_stats_content.append(html.Div([
            html.Span(t("travel_paid_label", lang),
                      style={"fontSize": "0.85rem", "color": "#475569", "fontWeight": "500"}),
            _comparison_badge(stats["paid_density"], stats["city_paid_density"], lang),
            html.Span(t("travel_city_avg", lang, avg=f"{stats['city_paid_density']:,}".replace(",", " ")),
                      style={"fontSize": "0.82rem", "color": "#94a3b8", "marginLeft": "0.4rem"}),
        ], className="d-flex align-items-center flex-wrap mb-2"))

    if stats["zone_types"]:
        zone_badges = [
            html.Span(
                f"{t(_ZONE_TYPE_KEYS.get(zt, 'zone_7'), lang)}: {n}",
                style={
                    "display": "inline-block",
                    "background": _ZONE_TYPE_COLORS.get(zt, "#64748b"),
                    "color": "white", "borderRadius": "8px", "padding": "3px 10px",
                    "fontSize": "0.82rem", "fontWeight": "700",
                    "marginRight": "0.4rem", "marginBottom": "0.3rem",
                },
            )
            for zt, n in stats["zone_types"].items()
        ]
        parking_stats_content.append(html.Div([
            html.Span(t("travel_zone_label", lang),
                      style={"fontSize": "0.85rem", "color": "#475569",
                             "fontWeight": "500", "marginRight": "0.3rem"}),
            *zone_badges,
        ], className="d-flex flex-wrap align-items-center mb-3"))
    else:
        parking_stats_content.append(html.Div([
            html.I(className="fa-solid fa-coins me-2", style={"color": "#94a3b8"}),
            html.Span(t("travel_no_zones", lang), style={"fontSize": "0.82rem", "color": "#94a3b8"}),
        ], className="mb-3"))

    return dbc.Row([
        dbc.Col([
            section_header(
                title=t("section_travel", lang),
                accent_color=theme.TRAVEL_ACCENT_COLOR,
                bg_color=theme.TRAVEL_BG_COLOR,
                text_color=theme.TRAVEL_TEXT_COLOR,
            ),
            *parking_stats_content,
            html.H6(t("travel_map_header", lang),
                    style={"color": theme.TRAVEL_TEXT_COLOR, "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem", "marginTop": "0.25rem"}),
            dbc.Row([dbc.Col(card, xs=6, sm=4, md=3, className="mb-3") for card in cards],
                    className="g-2 mb-2"),
        ], width=12)
    ])
