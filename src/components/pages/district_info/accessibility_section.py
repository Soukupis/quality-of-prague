"""Metro barrier-free and disabled parking accessibility section.

Operationalizes the WHOQOL Level of Independence domain and QOUL Mobility
dimension by analysing barrier-free metro access and disabled parking (ZTP)
provision per district.

Theory reference: Jan persona (age 75, Holešovice) — barrier-free transport
and nearby disabled parking spaces are prerequisites for independent mobility;
WBCSD mobility indicator on accessibility for reduced mobility.
"""
from dash import html
import dash_bootstrap_components as dbc
from src.components.ui import section_header, info_card_row, info_card
from src.utils.geospatial_utils import points_within_polygon
from src.utils.loaders.districts_loader import get_subway_entrances_data, get_ztp_parking_data
from src.utils.districts.district_utils import get_district_areas_km2
from src.components.config import theme


def _get_metro_accessibility_stats(district_polygon):
    """Compute barrier-free metro entrance statistics for a district.

    Args:
        district_polygon: Shapely polygon for the district boundary.

    Returns:
        dict with keys: total, elevator, escalator_no_lift, stairs_only,
        lift_ratio (%), line_counts (dict A/B/C).
    """
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

    # Count entrances per metro line (handles combined entries like 'A,B')
    line_counts = {"A": 0, "B": 0, "C": 0}
    for linka in within["vst_linka"].dropna():
        for line in str(linka).split(","):
            line = line.strip()
            if line in line_counts:
                line_counts[line] += 1

    return {
        "total": total,
        "elevator": has_elevator,
        "escalator_no_lift": escalator_no_lift,
        "stairs_only": stairs_only,
        "lift_ratio": lift_ratio,
        "line_counts": line_counts,
    }


def _ratio_badge(ratio):
    """Return a colored badge for the elevator accessibility ratio."""
    if ratio >= 50:
        color = "#059669"   # green
    elif ratio >= 25:
        color = "#d97706"   # amber
    else:
        color = "#dc2626"   # red

    return html.Span(
        f"{ratio} % bezbariérových vstupů",
        style={
            "display": "inline-block",
            "background": color,
            "color": "white",
            "borderRadius": "12px",
            "padding": "2px 10px",
            "fontSize": "0.82rem",
            "fontWeight": "600",
            "marginLeft": "0.5rem",
            "verticalAlign": "middle",
        }
    )


def _stat_card(icon_class, label, value, color="#334155"):
    """Compact read-only stat card (no layer toggle)."""
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
               "background": "linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%)"}
    )


def _metro_line_badge(line, count, color):
    return html.Span(
        f"Linka {line}: {count}",
        style={
            "display": "inline-block",
            "background": color,
            "color": "white",
            "borderRadius": "8px",
            "padding": "3px 10px",
            "fontSize": "0.82rem",
            "fontWeight": "700",
            "marginRight": "0.4rem",
        }
    )


LINE_COLORS = {"A": "#009900", "B": "#ffcc00", "C": "#cc0000"}
LINE_TEXT_COLORS = {"A": "white", "B": "#1e293b", "C": "white"}


def _get_ztp_stats(district, district_polygon):
    """Compute ZTP (disabled) parking statistics for a district.

    Args:
        district: District name string (for area lookup).
        district_polygon: Shapely polygon for the district boundary.

    Returns:
        dict with keys: locations, total_spaces, density_per_km2.
    """
    data = get_ztp_parking_data()
    within = points_within_polygon(district_polygon, data, "geometry")

    locations = len(within)
    total_spaces = int(within["pocet_ps"].sum()) if locations > 0 else 0

    areas = get_district_areas_km2()
    area_km2 = areas.get(district, 1.0)
    density = round(total_spaces / area_km2, 2) if area_km2 > 0 else 0.0

    return {"locations": locations, "total_spaces": total_spaces, "density_per_km2": density}


def accessibility_section(district, polygons):
    """Create the accessibility section for a district detail page.

    Shows barrier-free metro entrance analysis and ZTP (disabled) parking stats.
    Operationalizes the QOUL Mobility domain and WHOQOL Level of Independence.

    Args:
        district: Name of the district (e.g., "Praha 1").
        polygons: Dict mapping district names to Shapely polygon geometries.

    Returns:
        dbc.Row with the accessibility section, or None if no relevant data.
    """
    if district not in polygons:
        return None

    metro_stats = _get_metro_accessibility_stats(polygons[district])
    ztp_stats = _get_ztp_stats(district, polygons[district])

    if metro_stats["total"] == 0 and ztp_stats["locations"] == 0:
        return None

    # --- Metro elevator analysis ---
    metro_content = []
    if metro_stats["total"] > 0:
        line_badges = []
        for line, color in LINE_COLORS.items():
            count = metro_stats["line_counts"].get(line, 0)
            if count > 0:
                line_badges.append(html.Span(
                    f"Linka {line}: {count}",
                    style={
                        "display": "inline-block",
                        "background": color,
                        "color": LINE_TEXT_COLORS[line],
                        "borderRadius": "8px",
                        "padding": "3px 10px",
                        "fontSize": "0.82rem",
                        "fontWeight": "700",
                        "marginRight": "0.4rem",
                    }
                ))

        metro_content = [
            html.H6("Metro — bezbariérový přístup", style={"color": "#4c1d95", "fontWeight": "600",
                                                             "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
            dbc.Row([
                dbc.Col(_stat_card("fa-door-open", "Vstupů celkem", metro_stats["total"], "#3b82f6"),
                        xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_stat_card("fa-elevator", "S výtahem", metro_stats["elevator"], "#059669"),
                        xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_stat_card("fa-stairs", "Pouze schody", metro_stats["stairs_only"], "#dc2626"),
                        xs=6, sm=4, md=3, className="mb-3"),
            ], className="g-2 mb-2"),
            html.Div([
                html.Span("Podíl vstupů s výtahem:",
                          style={"fontSize": "0.85rem", "color": "#475569", "fontWeight": "500"}),
                _ratio_badge(metro_stats["lift_ratio"]),
            ], className="d-flex align-items-center mb-2"),
            dbc.Progress(
                value=metro_stats["lift_ratio"],
                max=100,
                color="success" if metro_stats["lift_ratio"] >= 50
                    else ("warning" if metro_stats["lift_ratio"] >= 25 else "danger"),
                style={"height": "10px", "borderRadius": "5px"},
                className="mb-3"
            ),
            html.Div([
                html.Span("Linky metra: ",
                          style={"fontSize": "0.85rem", "color": "#475569",
                                 "fontWeight": "500", "marginRight": "0.3rem"}),
                *line_badges,
            ], className="mb-3") if line_badges else None,
        ]

    # --- ZTP parking analysis ---
    ztp_content = []
    if ztp_stats["locations"] > 0:
        ztp_content = [
            html.H6("Parkování ZTP — vyhrazená místa",
                    style={"color": "#4c1d95", "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem", "marginTop": "0.75rem"}),
            dbc.Row([
                dbc.Col(_stat_card("fa-wheelchair", "Parkovišť", ztp_stats["locations"], "#7c3aed"),
                        xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_stat_card("fa-square-parking", "Míst celkem", ztp_stats["total_spaces"], "#5b21b6"),
                        xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_stat_card("fa-map", f"Míst / km²", f"{ztp_stats['density_per_km2']:.1f}", "#6d28d9"),
                        xs=6, sm=4, md=3, className="mb-3"),
            ], className="g-2 mb-2"),
        ]

    return dbc.Row([
        dbc.Col([
            section_header(
                title="Přístupnost",
                accent_color=theme.ACCESSIBILITY_ACCENT_COLOR,
                bg_color=theme.ACCESSIBILITY_BG_COLOR,
                text_color=theme.ACCESSIBILITY_TEXT_COLOR,
            ),
            *[c for c in metro_content if c is not None],
            *ztp_content,
        ], width=12)
    ])
