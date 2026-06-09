"""Demographic statistics section for district detail pages.

Operationalises the QOUL Socio-economic Security domain and OECD Better Life
Index normalisation by showing population structure per district. Elderly
population share (65+) is directly relevant to the Jan persona (age 75, Praha 7)
and to demand forecasting for barrier-free infrastructure.

Theory reference: Stiglitz-Sen-Fitoussi per-capita normalisation; OECD Better
Life Index denominator; Diener's SWB — age cohort composition shapes collective
well-being perception in a neighbourhood.
Source: ČSÚ annual demographic statistics, year 2024.
"""
from dash import html
import dash_bootstrap_components as dbc

from src.components.ui import section_header
from src.components.config import theme
from src.utils.loaders.xlsx_loader import get_district_demographics


def _demo_stat_card(icon_class, label, value, color="#78350f", small=False):
    return dbc.Card(
        dbc.CardBody(
            html.Div([
                html.I(className=f"fa-solid {icon_class}",
                       style={"fontSize": "1.3rem", "color": color, "minWidth": "1.6rem"}),
                html.Div([
                    html.Div(label, style={"fontSize": "0.8rem", "color": "#64748b",
                                           "fontWeight": "500", "lineHeight": "1.2"}),
                    html.Div(str(value),
                             style={"fontSize": "1.1rem" if small else "1.3rem",
                                    "fontWeight": "700", "color": "#1e293b",
                                    "lineHeight": "1.3"}),
                ], style={"marginLeft": "0.5rem"})
            ], className="d-flex align-items-center"),
        ),
        className="shadow-sm h-100",
        style={"border": "none", "borderRadius": "0.75rem",
               "background": "linear-gradient(135deg, #fffbeb 0%, #ffffff 100%)"}
    )


def _age_bar(age_0_14, age_15_64, age_65plus):
    """Stacked horizontal age distribution bar."""
    return html.Div([
        html.Div("Věková struktura obyvatelstva",
                 style={"fontSize": "0.82rem", "color": "#64748b", "fontWeight": "500",
                        "marginBottom": "0.3rem"}),
        html.Div([
            html.Div(
                f"{age_0_14:.1f}% (0–14)",
                style={
                    "width": f"{age_0_14:.1f}%",
                    "background": "#fbbf24",
                    "color": "#78350f",
                    "fontSize": "0.75rem",
                    "fontWeight": "600",
                    "padding": "2px 4px",
                    "overflow": "hidden",
                    "whiteSpace": "nowrap",
                    "minWidth": "40px",
                }
            ),
            html.Div(
                f"{age_15_64:.1f}% (15–64)",
                style={
                    "width": f"{age_15_64:.1f}%",
                    "background": "#3b82f6",
                    "color": "white",
                    "fontSize": "0.75rem",
                    "fontWeight": "600",
                    "padding": "2px 4px",
                    "overflow": "hidden",
                    "whiteSpace": "nowrap",
                }
            ),
            html.Div(
                f"{age_65plus:.1f}% (65+)",
                style={
                    "width": f"{age_65plus:.1f}%",
                    "background": "#8b5cf6",
                    "color": "white",
                    "fontSize": "0.75rem",
                    "fontWeight": "600",
                    "padding": "2px 4px",
                    "overflow": "hidden",
                    "whiteSpace": "nowrap",
                    "minWidth": "50px",
                }
            ),
        ], style={"display": "flex", "height": "24px", "borderRadius": "4px",
                  "overflow": "hidden", "marginBottom": "0.3rem"}),
        html.Div([
            html.Span("■ 0–14 ", style={"color": "#fbbf24", "fontSize": "0.75rem"}),
            html.Span("■ 15–64 ", style={"color": "#3b82f6", "fontSize": "0.75rem"}),
            html.Span("■ 65+ ", style={"color": "#8b5cf6", "fontSize": "0.75rem"}),
        ]),
    ], className="mb-3")


def _elderly_badge(pct_65plus):
    """Color-coded badge for elderly share — higher means more pressure on
    barrier-free infrastructure (Jan persona)."""
    if pct_65plus >= 20:
        color, label = "#7c3aed", "Vysoký podíl seniorů"
    elif pct_65plus >= 15:
        color, label = "#d97706", "Průměrný podíl seniorů"
    else:
        color, label = "#059669", "Nižší podíl seniorů"

    return html.Span(
        label,
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


def demographics_section(district: str, polygons: dict):
    """Create the demographic statistics section for a district detail page.

    Args:
        district: District name (e.g., "Praha 7").
        polygons: Dict mapping district names to Shapely polygon geometries
            (used only to verify the district exists).

    Returns:
        dbc.Row with the demographics section, or None if no data available.
    """
    if district not in polygons:
        return None

    demo = get_district_demographics(2024)
    data = demo.get(district)
    if not data:
        return None

    population = int(data.get("population", 0))
    pop_density = data.get("pop_density_per_km2", 0)
    age_0_14 = data.get("age_0_14_pct", 0)
    age_15_64 = data.get("age_15_64_pct", 0)
    age_65plus = data.get("age_65plus_pct", 0)
    mean_age = data.get("mean_age", 0)

    return dbc.Row([
        dbc.Col([
            section_header(
                title="Demografické údaje",
                accent_color=theme.DEMOGRAPHICS_ACCENT_COLOR,
                bg_color=theme.DEMOGRAPHICS_BG_COLOR,
                text_color=theme.DEMOGRAPHICS_TEXT_COLOR,
            ),
            html.H6("Obyvatelstvo (2024, ČSÚ)",
                    style={"color": theme.DEMOGRAPHICS_TEXT_COLOR, "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
            dbc.Row([
                dbc.Col(_demo_stat_card("fa-people-group", "Počet obyvatel",
                                        f"{population:,}".replace(",", " "), "#78350f"),
                        xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_demo_stat_card("fa-person-shelter", "Hustota (os/km²)",
                                        f"{pop_density:,.0f}".replace(",", " "), "#92400e"),
                        xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_demo_stat_card("fa-calendar", "Průměrný věk",
                                        f"{mean_age:.1f} let", "#b45309"),
                        xs=6, sm=4, md=3, className="mb-3"),
                dbc.Col(_demo_stat_card("fa-user-group", "Senioři (65+)",
                                        f"{age_65plus:.1f} %", "#7c3aed", small=True),
                        xs=6, sm=4, md=3, className="mb-3"),
            ], className="g-2 mb-2"),

            _age_bar(age_0_14, age_15_64, age_65plus),

            html.Div([
                html.Span("Podíl seniorů 65+: ",
                          style={"fontSize": "0.85rem", "color": "#475569", "fontWeight": "500"}),
                html.Span(f"{age_65plus:.1f} %",
                          style={"fontWeight": "700", "color": "#7c3aed", "marginRight": "0.25rem"}),
                _elderly_badge(age_65plus),
            ], className="d-flex align-items-center mb-2"),

            dbc.Alert([
                html.I(className="fa-solid fa-circle-info me-2", style={"color": "#b45309"}),
                html.Span("Podíl seniorů 65+ je klíčovým ukazatelem poptávky po bezbariérové "
                          "infrastruktuře (srov. persona Jan, 75 let). Vyšší hustota zalidnění "
                          "zvyšuje efektivitu sdílených služeb.",
                          style={"fontSize": "0.8rem", "color": "#374151"})
            ], color="warning",
               style={"padding": "0.5rem 0.75rem", "borderRadius": "0.5rem",
                      "background": "#fffbeb", "border": "1px solid #fde68a",
                      "fontSize": "0.8rem"}),
        ], width=12)
    ])
