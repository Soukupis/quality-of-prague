from dash import html
import dash_bootstrap_components as dbc

from src.components.ui import section_header
from src.components.config import theme
from src.utils.geospatial_utils import points_within_polygon
from src.utils.loaders.districts_loader import get_pid_stops_data, get_nextbike_data
from src.utils.districts.district_utils import get_district_areas_km2
from src.i18n import t


_TRAFFIC_COLORS = {
    "metro": "#cc0000",
    "metroA": "#009900",
    "metroB": "#ffcc00",
    "metroC": "#cc0000",
    "tram": "#e6a817",
    "bus": "#1d4ed8",
    "train": "#0f766e",
    "ferry": "#0284c7",
    "funicular": "#7c3aed",
}

_TRAFFIC_TEXT_COLORS = {
    "metroB": "#1e293b",
}

_KNOWN_MODES = set(_TRAFFIC_COLORS.keys())


def _get_pid_stats(district: str, district_polygon) -> dict:
    data = get_pid_stops_data()
    within = points_within_polygon(district_polygon, data, "geometry")
    total = len(within)

    if total == 0:
        return {"total": 0, "by_mode": {}, "wheelchair_yes": 0,
                "wheelchair_possible": 0, "density": 0.0}

    by_mode = {}
    for mode in _KNOWN_MODES:
        count = int((within["traffic_type"] == mode).sum())
        if count > 0:
            by_mode[mode] = count
    for mode in within["traffic_type"].dropna().unique():
        if mode not in _KNOWN_MODES:
            count = int((within["traffic_type"] == mode).sum())
            if count > 0:
                by_mode[mode] = count

    wheelchair_yes = int((within["wheelchair"] == "yes").sum())
    wheelchair_possible = int((within["wheelchair"] == "possible").sum())

    areas = get_district_areas_km2()
    area_km2 = areas.get(district, 1.0)
    density = round(total / area_km2, 1)

    return {
        "total": total,
        "by_mode": by_mode,
        "wheelchair_yes": wheelchair_yes,
        "wheelchair_possible": wheelchair_possible,
        "density": density,
    }


def _get_nextbike_stats(district_polygon) -> dict:
    data = get_nextbike_data()
    within = points_within_polygon(district_polygon, data, "geometry")
    count = len(within)
    total_capacity = int(within["capacity"].sum()) if count > 0 else 0
    avg_capacity = round(total_capacity / count, 1) if count > 0 else 0.0
    return {"count": count, "total_capacity": total_capacity, "avg_capacity": avg_capacity}


def _mob_stat_card(icon_class, label, value, color="#1e3a8a", small=False):
    return dbc.Card(
        dbc.CardBody(
            html.Div([
                html.I(className=f"fa-solid {icon_class}",
                       style={"fontSize": "1.3rem", "color": color, "minWidth": "1.6rem"}),
                html.Div([
                    html.Div(label, style={"fontSize": "0.8rem", "color": "#64748b",
                                           "fontWeight": "500", "lineHeight": "1.2"}),
                    html.Div(str(value), style={"fontSize": "1.1rem" if small else "1.3rem",
                                                "fontWeight": "700", "color": "#1e293b",
                                                "lineHeight": "1.3"}),
                ], style={"marginLeft": "0.5rem"})
            ], className="d-flex align-items-center"),
        ),
        className="shadow-sm h-100",
        style={"border": "none", "borderRadius": "0.75rem",
               "background": "linear-gradient(135deg, #eff6ff 0%, #ffffff 100%)"}
    )


def _mode_badge(mode: str, count: int, lang: str):
    color = _TRAFFIC_COLORS.get(mode, "#64748b")
    text_color = _TRAFFIC_TEXT_COLORS.get(mode, "white")
    mode_key = f"mode_{mode}"
    label = t(mode_key, lang) if f"mode_{mode}" in (
        "mode_metro", "mode_metroA", "mode_metroB", "mode_metroC",
        "mode_tram", "mode_bus", "mode_train", "mode_ferry", "mode_funicular"
    ) else mode
    label = t(mode_key, lang)
    return html.Span(
        f"{label}: {count}",
        style={
            "display": "inline-block", "background": color, "color": text_color,
            "borderRadius": "8px", "padding": "3px 10px",
            "fontSize": "0.82rem", "fontWeight": "700",
            "marginRight": "0.4rem", "marginBottom": "0.3rem",
        }
    )


def _wheelchair_ratio_badge(yes_count, possible_count, total, lang):
    accessible = yes_count + possible_count
    ratio = round(accessible / total * 100, 1) if total > 0 else 0.0
    color = "#059669" if ratio >= 50 else ("#d97706" if ratio >= 25 else "#dc2626")
    return html.Span(
        t("mob_wheelchair_badge", lang, ratio=ratio),
        style={
            "display": "inline-block", "background": color, "color": "white",
            "borderRadius": "12px", "padding": "2px 10px",
            "fontSize": "0.82rem", "fontWeight": "600",
            "marginLeft": "0.5rem", "verticalAlign": "middle",
        }
    )


def mobility_section(district: str, polygons: dict, lang: str = "cs"):
    if district not in polygons:
        return None

    polygon = polygons[district]
    pid = _get_pid_stats(district, polygon)
    nextbike = _get_nextbike_stats(polygon)

    if pid["total"] == 0 and nextbike["count"] == 0:
        return None

    pid_content = []
    if pid["total"] > 0:
        mode_badges = [
            _mode_badge(mode, cnt, lang)
            for mode, cnt in sorted(pid["by_mode"].items(), key=lambda x: -x[1])
            if mode in _KNOWN_MODES
        ]
        pid_content = [
            html.H6(t("mob_pid_header", lang),
                    style={"color": theme.MOBILITY_TEXT_COLOR, "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
            dbc.Row([
                dbc.Col(_mob_stat_card("fa-signs-post", t("mob_pid_total", lang),
                                       pid["total"], "#1d4ed8"),
                        xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_mob_stat_card("fa-map", t("mob_pid_density", lang),
                                       f"{pid['density']:.1f}", "#1e40af"),
                        xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_mob_stat_card("fa-wheelchair", t("mob_pid_wheelchair", lang),
                                       pid["wheelchair_yes"] + pid["wheelchair_possible"],
                                       "#7c3aed"),
                        xs=6, sm=4, md=3, className="mb-3"),
            ], className="g-2 mb-2"),
            html.Div([
                html.Span(t("mob_by_mode_label", lang),
                          style={"fontSize": "0.85rem", "color": "#475569",
                                 "fontWeight": "500", "marginRight": "0.3rem"}),
                *mode_badges,
            ], className="d-flex flex-wrap align-items-center mb-2"),
            html.Div([
                html.Span(t("mob_wheelchair_label", lang),
                          style={"fontSize": "0.85rem", "color": "#475569", "fontWeight": "500"}),
                _wheelchair_ratio_badge(pid["wheelchair_yes"], pid["wheelchair_possible"],
                                        pid["total"], lang),
            ], className="d-flex align-items-center mb-3"),
        ]

    nextbike_content = []
    if nextbike["count"] > 0:
        nextbike_content = [
            html.H6(t("mob_nextbike_header", lang),
                    style={"color": theme.MOBILITY_TEXT_COLOR, "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem",
                           "marginTop": "0.5rem" if pid_content else "0"}),
            dbc.Row([
                dbc.Col(_mob_stat_card("fa-bicycle", t("mob_nextbike_stations", lang),
                                       nextbike["count"], "#0891b2"),
                        xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_mob_stat_card("fa-circle-check", t("mob_nextbike_capacity", lang),
                                       nextbike["total_capacity"], "#0e7490"),
                        xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_mob_stat_card("fa-chart-simple", t("mob_nextbike_avg", lang),
                                       t("mob_nextbike_avg_unit", lang, avg=nextbike["avg_capacity"]),
                                       "#155e75", small=True),
                        xs=6, sm=4, md=3, className="mb-3"),
            ], className="g-2 mb-2"),
        ]
    elif pid_content:
        nextbike_content = [
            html.Div([
                html.I(className="fa-solid fa-bicycle me-2", style={"color": "#94a3b8"}),
                html.Span(t("mob_nextbike_none", lang),
                          style={"fontSize": "0.82rem", "color": "#94a3b8"}),
            ], className="mb-2"),
        ]

    return dbc.Row([
        dbc.Col([
            section_header(
                title=t("section_mobility", lang),
                accent_color=theme.MOBILITY_ACCENT_COLOR,
                bg_color=theme.MOBILITY_BG_COLOR,
                text_color=theme.MOBILITY_TEXT_COLOR,
            ),
            *pid_content,
            *nextbike_content,
        ], width=12)
    ])
