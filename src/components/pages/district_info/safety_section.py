from dash import html
import dash_bootstrap_components as dbc

from src.components.ui import info_card, section_header
from src.configs.dataset_config import DATASET_CONFIGS
from src.utils.geospatial_utils import point_count_for_polygon, points_within_polygon
from src.utils.loaders import get_police_stations_data
from src.utils.districts import get_district_areas_km2
from src.components.config import theme
from src.i18n import t


def _stat_card(icon_class, label, value, color="#b45309"):
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
               "background": "linear-gradient(135deg, #fffbf5 0%, #ffffff 100%)"},
    )


def _density_badge(district_density, city_density, lang):
    if city_density == 0:
        return None
    ratio = district_density / city_density
    if ratio >= 1.5:
        color, text = "#059669", t("density_above", lang, ratio=ratio)
    elif ratio >= 0.5:
        color, text = "#d97706", t("density_near", lang)
    else:
        color, text = "#dc2626", t("density_below", lang)
    return html.Span(
        text,
        style={
            "display": "inline-block", "background": color, "color": "white",
            "borderRadius": "12px", "padding": "2px 10px",
            "fontSize": "0.82rem", "fontWeight": "600",
            "marginLeft": "0.5rem", "verticalAlign": "middle",
        },
    )


def _get_safety_stats(district, district_polygon):
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
                cat = "service"
            elif "OŘ MP" in pozn:
                hq += 1
                cat = "hq"
            else:
                special += 1
                cat = "special"
            stations.append({"address": nvpk, "type": pozn, "category": cat})

    return {
        "count": count, "density": density, "city_density": city_density,
        "regular": regular, "hq": hq, "special": special, "stations": stations,
    }


_STATION_CATEGORY_STYLES = {
    "service":  ("#fef3c7", "#92400e"),
    "hq":       ("#fce7f3", "#9d174d"),
    "special":  ("#ede9fe", "#5b21b6"),
}
_TYPE_BADGE_COLORS = {"service": "#b45309", "hq": "#9d174d", "special": "#5b21b6"}


def _station_row(station):
    bg, fg = _STATION_CATEGORY_STYLES.get(station["category"], ("#f1f5f9", "#334155"))
    return html.Tr([
        html.Td(
            html.I(className="fa-solid fa-building-shield",
                   style={"color": "#b45309", "fontSize": "0.9rem"}),
            style={"paddingRight": "0.75rem", "paddingBottom": "0.5rem", "verticalAlign": "middle"},
        ),
        html.Td(station["address"],
                style={"fontSize": "0.85rem", "fontWeight": "500", "color": "#1e293b",
                       "paddingRight": "1rem", "paddingBottom": "0.5rem"}),
        html.Td(
            html.Span(station["category_label"],
                      style={"fontSize": "0.75rem", "background": bg, "color": fg,
                             "borderRadius": "8px", "padding": "2px 8px", "fontWeight": "600"}),
            style={"paddingBottom": "0.5rem", "whiteSpace": "nowrap"},
        ),
    ], style={"borderBottom": "1px solid #f1f5f9"})


def safety_section(district, polygons, lang="cs"):
    police_stations = get_police_stations_data()

    cards = []
    for dataset_key, config in DATASET_CONFIGS.items():
        if config.get("section") == "safety":
            if dataset_key == "police_stations":
                count = point_count_for_polygon(polygons[district], police_stations, "geometry")
                cards.append(info_card(
                    config["icon"], config["title"], count, "info",
                    card_id=config["id"], dataset_key=dataset_key,
                    compact=True, color=config.get("color", "#334155"),
                ))

    if not cards:
        return None

    stats = _get_safety_stats(district, polygons[district])

    cat_labels = {
        "service": t("safety_cat_service", lang),
        "hq":      t("safety_cat_hq", lang),
        "special": t("safety_cat_special", lang),
    }
    for s in stats["stations"]:
        s["category_label"] = cat_labels.get(s["category"], s["category"])

    stats_content = [
        html.H6(t("safety_police_coverage", lang),
                style={"color": theme.SAFETY_TEXT_COLOR, "fontWeight": "600",
                       "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
        dbc.Row([
            dbc.Col(_stat_card("fa-building-shield", t("safety_stations_total", lang),
                               stats["count"], "#b45309"), xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_stat_card("fa-map", t("safety_stations_density", lang),
                               f"{stats['density']:.3f}", "#92400e"), xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_stat_card("fa-city", t("safety_prague_avg", lang),
                               f"{stats['city_density']:.3f}", "#78350f"), xs=6, sm=4, md=3, className="mb-3"),
        ], className="g-2 mb-2"),
    ]

    stats_content.append(html.Div([
        html.Span(t("safety_coverage_label", lang),
                  style={"fontSize": "0.85rem", "color": "#475569", "fontWeight": "500"}),
        _density_badge(stats["density"], stats["city_density"], lang),
    ], className="d-flex align-items-center mb-3"))

    if stats["count"] > 1:
        type_badges = []
        for key, label_key in [("regular", "safety_cat_service"), ("hq", "safety_cat_hq"), ("special", "safety_cat_special")]:
            n = stats[key]
            if n > 0:
                type_badges.append(html.Span(
                    f"{t(label_key, lang)}: {n}",
                    style={
                        "display": "inline-block",
                        "background": _TYPE_BADGE_COLORS[{"regular": "service", "hq": "hq", "special": "special"}[key]],
                        "color": "white", "borderRadius": "8px", "padding": "3px 10px",
                        "fontSize": "0.82rem", "fontWeight": "700",
                        "marginRight": "0.4rem", "marginBottom": "0.3rem",
                    },
                ))
        if type_badges:
            stats_content.append(html.Div([
                html.Span(t("safety_types_label", lang),
                          style={"fontSize": "0.85rem", "color": "#475569",
                                 "fontWeight": "500", "marginRight": "0.3rem"}),
                *type_badges,
            ], className="d-flex flex-wrap align-items-center mb-3"))
    elif stats["count"] == 0:
        stats_content.append(html.Div([
            html.I(className="fa-solid fa-building-shield me-2", style={"color": "#94a3b8"}),
            html.Span(t("safety_no_stations", lang), style={"fontSize": "0.82rem", "color": "#94a3b8"}),
        ], className="mb-3"))

    station_table_content = []
    if 0 < stats["count"] <= 15:
        station_table_content = [
            html.H6(t("safety_table_header", lang),
                    style={"color": theme.SAFETY_TEXT_COLOR, "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
            html.Div(
                html.Table(
                    [html.Tbody([_station_row(s) for s in stats["stations"]])],
                    style={"width": "100%", "borderCollapse": "collapse"},
                ),
                style={"background": "#f8fafc", "borderRadius": "0.75rem",
                       "padding": "0.75rem 1rem", "marginBottom": "0.75rem"},
            ),
        ]

    return dbc.Row([
        dbc.Col([
            section_header(
                title=t("section_safety", lang),
                accent_color=theme.SAFETY_ACCENT_COLOR,
                bg_color=theme.SAFETY_BG_COLOR,
                text_color=theme.SAFETY_TEXT_COLOR,
            ),
            *stats_content,
            *station_table_content,
            html.H6(t("safety_map_header", lang),
                    style={"color": theme.SAFETY_TEXT_COLOR, "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem", "marginTop": "0.25rem"}),
            dbc.Row([dbc.Col(card, xs=6, sm=4, md=3, className="mb-3") for card in cards],
                    className="g-2 mb-2"),
        ], width=12)
    ])
