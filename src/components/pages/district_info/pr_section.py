"""Park and Ride (P+R) capacity and intermodality section.

Operationalizes the QOUL Mobility domain — specifically the intermodality
and commute-time dimensions from WBCSD mobility indicators.

P+R facilities enable seamless car-to-transit transfer (intermodality),
reducing dependency on private cars for the full journey. The planned
capacity (kapacita_vyhled) shows the city's investment direction.

Theory reference: WBCSD intermodality indicator; QOUL Mobility domain;
Elena persona (metro + bike intermodality).
"""
from dash import html
import dash_bootstrap_components as dbc
from src.components.ui import section_header
from src.utils.geospatial_utils import points_within_polygon
from src.utils.loaders.districts_loader import get_parking_p_r_data
from src.components.config import theme

# stav field mapping (from data exploration)
STAV_LABELS = {1: "V provozu", 4: "Plánováno", 5: "V provozu"}


def _get_pr_stats(district_polygon):
    """Compute P+R capacity statistics for a district.

    Args:
        district_polygon: Shapely polygon for the district boundary.

    Returns:
        dict with keys: count, current_capacity, planned_capacity, facilities (list).
    """
    data = get_parking_p_r_data()
    within = points_within_polygon(district_polygon, data, "geometry")

    if len(within) == 0:
        return None

    current_capacity = int(within["kapacita"].fillna(0).sum())
    planned_mask = within["kapacita_vyhled"].notna() & (within["kapacita_vyhled"] > 0)
    planned_capacity = int(within.loc[planned_mask, "kapacita_vyhled"].sum())

    facilities = []
    for _, row in within.iterrows():
        name = row.get("nazev", "—")
        cap = int(row["kapacita"]) if not (hasattr(row["kapacita"], "__float__") and
                                            row["kapacita"] != row["kapacita"]) else 0
        planned = int(row["kapacita_vyhled"]) if (
            row.get("kapacita_vyhled") and row["kapacita_vyhled"] == row["kapacita_vyhled"]
        ) else None
        stav = STAV_LABELS.get(int(row.get("stav", 1)), "—")
        facilities.append({"name": name, "capacity": cap, "planned": planned, "stav": stav})

    return {
        "count": len(within),
        "current_capacity": current_capacity,
        "planned_capacity": planned_capacity,
        "facilities": facilities,
    }


def _facility_row(facility):
    """Render one P+R facility as a compact table row."""
    planned_badge = html.Span(
        f"→ {facility['planned']} plán.",
        style={"fontSize": "0.75rem", "color": "#059669",
               "fontWeight": "600", "marginLeft": "0.4rem"}
    ) if facility["planned"] else None

    return html.Tr([
        html.Td(facility["name"],
                style={"fontSize": "0.85rem", "fontWeight": "500", "color": "#1e293b", "paddingRight": "1rem"}),
        html.Td([
            html.Span(f"{facility['capacity']} míst",
                      style={"fontSize": "0.85rem", "color": "#475569"}),
            planned_badge,
        ], style={"whiteSpace": "nowrap"}),
        html.Td(
            html.Span(facility["stav"],
                      style={"fontSize": "0.75rem", "background": "#dcfce7", "color": "#15803d",
                             "borderRadius": "8px", "padding": "2px 8px", "fontWeight": "600"}),
        ),
    ], style={"borderBottom": "1px solid #f1f5f9"})


def pr_section(district, polygons):
    """Create the P+R capacity section for a district detail page.

    Only renders if the district contains at least one P+R facility.

    Args:
        district: Name of the district (e.g., "Praha 10").
        polygons: Dict mapping district names to Shapely polygon geometries.

    Returns:
        dbc.Row with the P+R section, or None if no P+R in district.
    """
    if district not in polygons:
        return None

    stats = _get_pr_stats(polygons[district])
    if stats is None:
        return None

    summary_cards = dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody(html.Div([
                html.I(className="fa-solid fa-car-side",
                       style={"fontSize": "1.3rem", "color": "#0f766e", "minWidth": "1.6rem"}),
                html.Div([
                    html.Div("Parkovišť P+R", style={"fontSize": "0.8rem", "color": "#64748b", "fontWeight": "500"}),
                    html.Div(str(stats["count"]),
                             style={"fontSize": "1.3rem", "fontWeight": "700", "color": "#1e293b"}),
                ], style={"marginLeft": "0.5rem"})
            ], className="d-flex align-items-center")),
            className="shadow-sm h-100",
            style={"border": "none", "borderRadius": "0.75rem",
                   "background": "linear-gradient(135deg, #f0fdfa 0%, #ffffff 100%)"}),
            xs=6, sm=4, md=3, className="mb-3"
        ),
        dbc.Col(
            dbc.Card(dbc.CardBody(html.Div([
                html.I(className="fa-solid fa-square-parking",
                       style={"fontSize": "1.3rem", "color": "#0f766e", "minWidth": "1.6rem"}),
                html.Div([
                    html.Div("Kapacita celkem", style={"fontSize": "0.8rem", "color": "#64748b", "fontWeight": "500"}),
                    html.Div(f"{stats['current_capacity']} míst",
                             style={"fontSize": "1.3rem", "fontWeight": "700", "color": "#1e293b"}),
                ], style={"marginLeft": "0.5rem"})
            ], className="d-flex align-items-center")),
            className="shadow-sm h-100",
            style={"border": "none", "borderRadius": "0.75rem",
                   "background": "linear-gradient(135deg, #f0fdfa 0%, #ffffff 100%)"}),
            xs=6, sm=4, md=3, className="mb-3"
        ),
    ] + ([
        dbc.Col(
            dbc.Card(dbc.CardBody(html.Div([
                html.I(className="fa-solid fa-chart-line",
                       style={"fontSize": "1.3rem", "color": "#059669", "minWidth": "1.6rem"}),
                html.Div([
                    html.Div("Plánovaná kapacita", style={"fontSize": "0.8rem", "color": "#64748b", "fontWeight": "500"}),
                    html.Div(f"{stats['planned_capacity']} míst",
                             style={"fontSize": "1.3rem", "fontWeight": "700", "color": "#059669"}),
                ], style={"marginLeft": "0.5rem"})
            ], className="d-flex align-items-center")),
            className="shadow-sm h-100",
            style={"border": "none", "borderRadius": "0.75rem",
                   "background": "linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%)"}),
            xs=6, sm=4, md=3, className="mb-3"
        )
    ] if stats["planned_capacity"] > 0 else []), className="g-2 mb-3")

    facility_table = html.Div([
        html.H6("Přehled parkovišť P+R",
                style={"color": "#134e4a", "fontWeight": "600", "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
        html.Table(
            [html.Tbody([_facility_row(f) for f in stats["facilities"]])],
            style={"width": "100%", "borderCollapse": "collapse"}
        )
    ], style={"background": "#f8fafc", "borderRadius": "0.75rem", "padding": "0.75rem 1rem",
              "marginBottom": "0.5rem"})

    return dbc.Row([
        dbc.Col([
            section_header(
                title="Intermodalita (P+R)",
                accent_color=theme.TRAVEL_ACCENT_COLOR,
                bg_color=theme.TRAVEL_BG_COLOR,
                text_color=theme.TRAVEL_TEXT_COLOR,
            ),
            summary_cards,
            facility_table,
        ], width=12)
    ])