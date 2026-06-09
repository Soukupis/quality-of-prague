from dash import html
import dash_bootstrap_components as dbc
from src.components.ui import section_header, info_card_row, info_card
from src.utils.geospatial_utils import points_within_polygon
from src.utils.loaders.districts_loader import get_subway_entrances_data, get_ztp_parking_data
from src.utils.districts.district_utils import get_district_areas_km2
from src.components.config import theme
from src.i18n import t


def _get_metro_accessibility_stats(district_polygon):
    data = get_subway_entrances_data()
    within = points_within_polygon(district_polygon, data, "geometry")
    total = len(within)

    if total == 0:
        return {"total": 0, "elevator": 0, "escalator_no_lift": 0,
                "stairs_only": 0, "lift_ratio": 0.0, "line_counts": {}}

    has_elevator = int((within["vst_vytah"] > 0).sum())
    has_escalator = int((within["vst_eskal"] > 0).sum())
    escalator_no_lift = max(0, has_escalator - has_elevator)
    stairs_only = int(((within["vst_vytah"] == 0) & (within["vst_eskal"] == 0)).sum())
    lift_ratio = round(has_elevator / total * 100, 1)

    line_counts = {"A": 0, "B": 0, "C": 0}
    for linka in within["vst_linka"].dropna():
        for line in str(linka).split(","):
            line = line.strip()
            if line in line_counts:
                line_counts[line] += 1

    return {
        "total": total, "elevator": has_elevator,
        "escalator_no_lift": escalator_no_lift, "stairs_only": stairs_only,
        "lift_ratio": lift_ratio, "line_counts": line_counts,
    }


def _ratio_badge(ratio, lang):
    color = "#059669" if ratio >= 50 else ("#d97706" if ratio >= 25 else "#dc2626")
    return html.Span(
        t("access_ratio_badge", lang, ratio=ratio),
        style={
            "display": "inline-block", "background": color, "color": "white",
            "borderRadius": "12px", "padding": "2px 10px",
            "fontSize": "0.82rem", "fontWeight": "600",
            "marginLeft": "0.5rem", "verticalAlign": "middle",
        },
    )


def _stat_card(icon_class, label, value, color="#334155"):
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
               "background": "linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%)"},
    )


LINE_COLORS = {"A": "#009900", "B": "#ffcc00", "C": "#cc0000"}
LINE_TEXT_COLORS = {"A": "white", "B": "#1e293b", "C": "white"}


def _get_ztp_stats(district, district_polygon):
    data = get_ztp_parking_data()
    within = points_within_polygon(district_polygon, data, "geometry")
    locations = len(within)
    total_spaces = int(within["pocet_ps"].sum()) if locations > 0 else 0
    areas = get_district_areas_km2()
    area_km2 = areas.get(district, 1.0)
    density = round(total_spaces / area_km2, 2) if area_km2 > 0 else 0.0
    return {"locations": locations, "total_spaces": total_spaces, "density_per_km2": density}


def accessibility_section(district, polygons, lang="cs"):
    if district not in polygons:
        return None

    metro_stats = _get_metro_accessibility_stats(polygons[district])
    ztp_stats = _get_ztp_stats(district, polygons[district])

    if metro_stats["total"] == 0 and ztp_stats["locations"] == 0:
        return None

    metro_content = []
    if metro_stats["total"] > 0:
        line_badges = []
        for line, color in LINE_COLORS.items():
            count = metro_stats["line_counts"].get(line, 0)
            if count > 0:
                line_badges.append(html.Span(
                    t("access_line_badge", lang, line=line, count=count),
                    style={
                        "display": "inline-block", "background": color,
                        "color": LINE_TEXT_COLORS[line], "borderRadius": "8px",
                        "padding": "3px 10px", "fontSize": "0.82rem", "fontWeight": "700",
                        "marginRight": "0.4rem",
                    },
                ))

        metro_content = [
            html.H6(t("access_metro_header", lang),
                    style={"color": "#4c1d95", "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
            dbc.Row([
                dbc.Col(_stat_card("fa-door-open", t("access_metro_total", lang),
                                   metro_stats["total"], "#3b82f6"), xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_stat_card("fa-elevator", t("access_metro_elevator", lang),
                                   metro_stats["elevator"], "#059669"), xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_stat_card("fa-stairs", t("access_metro_stairs", lang),
                                   metro_stats["stairs_only"], "#dc2626"), xs=6, sm=4, md=3, className="mb-3"),
            ], className="g-2 mb-2"),
            html.Div([
                html.Span(t("access_ratio_label", lang),
                          style={"fontSize": "0.85rem", "color": "#475569", "fontWeight": "500"}),
                _ratio_badge(metro_stats["lift_ratio"], lang),
            ], className="d-flex align-items-center mb-2"),
            dbc.Progress(
                value=metro_stats["lift_ratio"], max=100,
                color="success" if metro_stats["lift_ratio"] >= 50
                    else ("warning" if metro_stats["lift_ratio"] >= 25 else "danger"),
                style={"height": "10px", "borderRadius": "5px"},
                className="mb-3",
            ),
        ]
        if line_badges:
            metro_content.append(html.Div([
                html.Span(t("access_lines_label", lang),
                          style={"fontSize": "0.85rem", "color": "#475569",
                                 "fontWeight": "500", "marginRight": "0.3rem"}),
                *line_badges,
            ], className="mb-3"))

    ztp_content = []
    if ztp_stats["locations"] > 0:
        ztp_content = [
            html.H6(t("access_ztp_header", lang),
                    style={"color": "#4c1d95", "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem", "marginTop": "0.75rem"}),
            dbc.Row([
                dbc.Col(_stat_card("fa-wheelchair", t("access_ztp_locations", lang),
                                   ztp_stats["locations"], "#7c3aed"), xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_stat_card("fa-square-parking", t("access_ztp_total", lang),
                                   ztp_stats["total_spaces"], "#5b21b6"), xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_stat_card("fa-map", t("access_ztp_density", lang),
                                   f"{ztp_stats['density_per_km2']:.1f}", "#6d28d9"),
                        xs=6, sm=4, md=3, className="mb-3"),
            ], className="g-2 mb-2"),
        ]

    return dbc.Row([
        dbc.Col([
            section_header(
                title=t("section_accessibility", lang),
                accent_color=theme.ACCESSIBILITY_ACCENT_COLOR,
                bg_color=theme.ACCESSIBILITY_BG_COLOR,
                text_color=theme.ACCESSIBILITY_TEXT_COLOR,
            ),
            *[c for c in metro_content if c is not None],
            *ztp_content,
        ], width=12)
    ])
