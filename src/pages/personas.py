"""Persona-based QoL dashboard page.

Demonstrates the thesis 'bottom-up' approach: the same objective urban
data produces different QoL implications depending on who lives in the city.
Three personas from the thesis are shown, each with their home district's
specific data filtered to their relevant QoL concerns.

Theory reference: Chapter 5 scenario case studies; Marans (2012) dual-
methodological framework; Diener's SWB bottom-up approach.
"""
import dash_bootstrap_components as dbc
from dash import register_page, html, dcc, callback, Input, Output, State

from src.components.ui import page_title
from src.utils.districts.district_utils import (
    get_district_polygons, get_points_in_district, get_district_areas_km2
)
from src.utils.loaders.districts_loader import get_subway_entrances_data, get_ztp_parking_data
from src.utils.geospatial_utils import points_within_polygon
from src.components.pages.district_info.accessibility_section import (
    _get_metro_accessibility_stats, _get_ztp_stats
)
from src.components.pages.district_info.pr_section import _get_pr_stats

register_page(__name__, path="/personas", name="Persony")

# ── Persona definitions ───────────────────────────────────────────────────────

PERSONAS = {
    "jan": {
        "id": "jan",
        "name": "Jan",
        "age": 75,
        "district": "Praha 7",
        "neighborhood": "Holešovice",
        "icon": "fa-person-cane",
        "color": "#0f766e",
        "bg": "#f0fdfa",
        "border": "#d1fae5",
        "description": "Důchodce, který je závislý na veřejné dopravě a potřebuje "
                        "bezbariérový přístup. Tráví čas v Stromovce. V létě trpí "
                        "efektem tepelného ostrova na zpevněných plochách.",
        "concerns": [
            ("fa-elevator", "Výtahy v metru", "Dostupnost bez schodů"),
            ("fa-wheelchair", "Parkoviště ZTP", "Počet vyhrazených míst"),
            ("fa-shield-halved", "Bezpečnost", "Policejní stanice v blízkosti"),
            ("fa-train-subway", "Dostupnost MHD", "Vstupy do metra"),
        ],
        "relevant_metrics": ["subway_entrances", "ztp_parking", "police_stations"],
    },
    "elena": {
        "id": "elena",
        "name": "Elena",
        "age": 28,
        "district": "Praha 8",
        "neighborhood": "Karlín",
        "icon": "fa-person-biking",
        "color": "#1d4ed8",
        "bg": "#eff6ff",
        "border": "#dbeafe",
        "description": "Tech profesionálka kombinující metro a sdílené kolo. "
                        "Oceňuje pěší dostupnost smíšené zástavby. Výzvy: "
                        "kvalita ovzduší a bezpečnost cyklostezek.",
        "concerns": [
            ("fa-train-subway", "Metro a intermodalita", "Počet vstupů a linek"),
            ("fa-car-side", "P+R a parkování", "Intermodální přestup"),
            ("fa-parking", "Parkovací automaty", "Hustota placených zón"),
            ("fa-shield-halved", "Bezpečnost", "Policejní stanice"),
        ],
        "relevant_metrics": ["subway_entrances", "parking_meters", "police_stations"],
    },
    "novak": {
        "id": "novak",
        "name": "Rodina Novákových",
        "age": None,
        "district": "Praha 6",
        "neighborhood": "Dejvice",
        "icon": "fa-people-roof",
        "color": "#b45309",
        "bg": "#fffbeb",
        "border": "#fde68a",
        "description": "Pár ve 30 letech se dvěma dětmi. Klíčové: školy, dětský lékař, "
                        "bezpečné hřiště. Obavy z PM2.5 u Evropské ulice. "
                        "Potřebují bezbariérový přístup s kočárkem.",
        "concerns": [
            ("fa-shield-halved", "Bezpečnost a policie", "Stanice v obvodě"),
            ("fa-wheelchair", "Přístupnost (kočárek)", "Parkoviště ZTP a výtahy"),
            ("fa-train-subway", "MHD dostupnost", "Vstupy do metra"),
            ("fa-wind", "Kvalita ovzduší", "PM2.5 u Evropské (data chybí)"),
        ],
        "relevant_metrics": ["police_stations", "subway_entrances", "ztp_parking"],
    }
}


def _persona_selector_card(persona, is_selected):
    p = PERSONAS[persona]
    selected_style = {
        "border": f"2px solid {p['color']}",
        "background": p["bg"],
        "cursor": "pointer",
        "borderRadius": "1rem",
        "transition": "all 0.2s ease",
    }
    normal_style = {
        "border": "2px solid #e2e8f0",
        "background": "white",
        "cursor": "pointer",
        "borderRadius": "1rem",
        "transition": "all 0.2s ease",
    }
    return html.A(
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.I(className=f"fa-solid {p['icon']}",
                           style={"fontSize": "2rem", "color": p["color"],
                                  "marginRight": "0.75rem"}),
                    html.Div([
                        html.Div(p["name"], style={"fontWeight": "700", "fontSize": "1rem",
                                                   "color": "#1e293b"}),
                        html.Div(
                            f"{'%d let — ' % p['age'] if p['age'] else ''}{p['neighborhood']}, {p['district']}",
                            style={"fontSize": "0.8rem", "color": "#64748b"}
                        ),
                    ])
                ], className="d-flex align-items-center mb-2"),
                html.P(p["description"], style={"fontSize": "0.8rem", "color": "#475569",
                                                  "lineHeight": "1.4", "marginBottom": 0})
            ])
        ], style=selected_style if is_selected else normal_style, className="shadow-sm h-100"),
        href=f"/personas?persona={persona}",
        style={"textDecoration": "none"}
    )


def _concern_row(icon_class, title, subtitle, color):
    return html.Div([
        html.I(className=f"fa-solid {icon_class}",
               style={"fontSize": "1.1rem", "color": color, "minWidth": "1.5rem"}),
        html.Div([
            html.Span(title, style={"fontWeight": "600", "fontSize": "0.85rem", "color": "#1e293b"}),
            html.Span(f" — {subtitle}", style={"fontSize": "0.82rem", "color": "#64748b"}),
        ], style={"marginLeft": "0.5rem"})
    ], className="d-flex align-items-center mb-2")


def _metric_card(icon_class, label, value, sub, color):
    return dbc.Card(
        dbc.CardBody(html.Div([
            html.I(className=f"fa-solid {icon_class}",
                   style={"fontSize": "1.4rem", "color": color, "minWidth": "1.8rem"}),
            html.Div([
                html.Div(label, style={"fontSize": "0.78rem", "color": "#64748b",
                                       "fontWeight": "500", "lineHeight": "1.2"}),
                html.Div(str(value), style={"fontSize": "1.4rem", "fontWeight": "700",
                                            "color": "#1e293b", "lineHeight": "1.3"}),
                html.Div(sub, style={"fontSize": "0.75rem", "color": "#94a3b8"}) if sub else None,
            ], style={"marginLeft": "0.5rem"})
        ], className="d-flex align-items-start")),
        className="shadow-sm h-100",
        style={"border": "none", "borderRadius": "0.75rem", "background": "white"}
    )


def _build_persona_detail(persona_id):
    """Build the full persona detail section with live data."""
    if persona_id not in PERSONAS:
        return None

    p = PERSONAS[persona_id]
    polygons = get_district_polygons()
    district = p["district"]

    if district not in polygons:
        return html.P(f"Data pro obvod {district} nejsou k dispozici.")

    polygon = polygons[district]
    areas = get_district_areas_km2()
    area_km2 = areas.get(district, 1.0)

    # Compute relevant metrics
    metro_stats = _get_metro_accessibility_stats(polygon)
    ztp_stats = _get_ztp_stats(district, polygon)
    police_count = len(get_points_in_district(district, "police_stations"))
    metro_count = metro_stats["total"]

    # Build metric cards based on persona
    metric_cards = []

    if persona_id == "jan":
        metric_cards = [
            dbc.Col(_metric_card("fa-train-subway", "Vstupy do metra", metro_count,
                                  f"v obvodu {district}", p["color"]),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-elevator", "Vstupy s výtahem",
                                  f"{metro_stats['elevator']} ({metro_stats['lift_ratio']}%)",
                                  "bezbariérový přístup", "#059669"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-wheelchair", "Místa ZTP",
                                  ztp_stats["total_spaces"],
                                  f"{ztp_stats['density_per_km2']:.1f} / km²", "#7c3aed"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-building-shield", "Policejní stanice",
                                  police_count,
                                  f"{round(police_count / area_km2, 2):.2f} / km²", "#dc2626"),
                    xs=6, sm=4, md=3, className="mb-3"),
        ]
        insight = (
            f"Jan žije v {p['neighborhood']} ({district}). "
            f"Obvod má {metro_count} vstupů do metra, z nichž pouze "
            f"{metro_stats['lift_ratio']}% disponuje výtahem. "
            f"Pro seniora se sníženou pohyblivostí to znamená, že "
            f"{metro_stats['stairs_only']} vstupů je dostupných jen po schodech — "
            f"přímý dopad na nezávislost a WHOQOL doménu 'Úroveň nezávislosti'."
        )

    elif persona_id == "elena":
        parking_count = len(get_points_in_district(district, "parking_meters"))
        pr_stats = _get_pr_stats(polygon)
        pr_count = pr_stats["count"] if pr_stats else 0
        pr_capacity = pr_stats["current_capacity"] if pr_stats else 0
        metric_cards = [
            dbc.Col(_metric_card("fa-train-subway", "Vstupy do metra", metro_count,
                                  f"linky: {', '.join([l for l, c in metro_stats['line_counts'].items() if c > 0])}",
                                  p["color"]),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-car-side", "Parkoviště P+R", pr_count,
                                  f"kapacita: {pr_capacity} míst" if pr_capacity else "žádné v obvodu",
                                  "#0f766e"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-parking", "Parkovací automaty",
                                  parking_count,
                                  f"{round(parking_count / area_km2, 1):.1f} / km²", "#8B008B"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-building-shield", "Policejní stanice",
                                  police_count,
                                  f"{round(police_count / area_km2, 2):.2f} / km²", "#dc2626"),
                    xs=6, sm=4, md=3, className="mb-3"),
        ]
        lines_str = ", ".join([f"Linka {l}" for l, c in metro_stats["line_counts"].items() if c > 0])
        insight = (
            f"Elena bydlí v {p['neighborhood']} ({district}). "
            f"Její obvod nabízí {metro_count} vstupů do metra ({lines_str}), "
            f"což umožňuje intermodální přestup. "
            f"Hustota parkovacích automatů ({round(parking_count / area_km2, 1):.1f}/km²) "
            f"odráží míru urbanizace a tlak na veřejný prostor — "
            f"relevantní pro QOUL dimenzi Mobility."
        )

    else:  # novak
        metric_cards = [
            dbc.Col(_metric_card("fa-building-shield", "Policejní stanice",
                                  police_count,
                                  f"{round(police_count / area_km2, 2):.2f} / km²", p["color"]),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-train-subway", "Vstupy do metra", metro_count,
                                  f"v obvodu {district}", "#1d4ed8"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-wheelchair", "Místa ZTP",
                                  ztp_stats["total_spaces"],
                                  f"{ztp_stats['density_per_km2']:.1f} / km²", "#7c3aed"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-elevator", "Metro s výtahem",
                                  f"{metro_stats['elevator']} ({metro_stats['lift_ratio']}%)",
                                  "přístup s kočárkem", "#059669"),
                    xs=6, sm=4, md=3, className="mb-3"),
        ]
        insight = (
            f"Rodina Novákových bydlí v {p['neighborhood']} ({district}). "
            f"Praha 6 zahrnuje Evropskou třídu — jednu z nejvíce exponovaných ulic "
            f"z hlediska PM2.5 a NO₂ v Praze (data Golemio, chybí v tomto dashboardu). "
            f"Přístupnost kočárku závisí na výtazích v metru: "
            f"{metro_stats['lift_ratio']}% vstupů je bezbariérových."
        )

    concerns_section = html.Div([
        html.H6("Klíčové QoL faktory pro tuto personu",
                style={"fontWeight": "700", "color": "#334155",
                       "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
        *[_concern_row(icon, title, sub, p["color"]) for icon, title, sub in p["concerns"]]
    ], style={"background": p["bg"], "borderRadius": "0.75rem",
              "padding": "0.85rem 1rem", "marginBottom": "1rem"})

    insight_box = html.Div([
        html.I(className="fa-solid fa-lightbulb",
               style={"color": "#f59e0b", "marginRight": "0.5rem", "fontSize": "1rem"}),
        html.Span(insight, style={"fontSize": "0.87rem", "color": "#475569", "lineHeight": "1.5"}),
    ], className="d-flex align-items-start",
       style={"background": "#fffbeb", "borderLeft": f"4px solid {p['color']}",
              "padding": "0.75rem 1rem", "borderRadius": "0 0.5rem 0.5rem 0",
              "marginTop": "0.5rem"})

    return html.Div([
        html.Div([
            html.I(className=f"fa-solid {p['icon']}",
                   style={"fontSize": "2.5rem", "color": p["color"], "marginRight": "0.75rem"}),
            html.Div([
                html.H3(p["name"], style={"fontWeight": "800", "color": "#1e293b", "marginBottom": "0.1rem"}),
                html.Span(
                    f"{'%d let · ' % p['age'] if p['age'] else ''}{p['neighborhood']}, {p['district']}",
                    style={"fontSize": "0.95rem", "color": "#64748b"}
                ),
            ])
        ], className="d-flex align-items-center mb-3",
           style={"borderBottom": f"3px solid {p['color']}", "paddingBottom": "0.75rem"}),

        html.P(p["description"], style={"fontSize": "0.95rem", "color": "#475569",
                                          "lineHeight": "1.6", "marginBottom": "1rem"}),
        concerns_section,

        html.H6("Data pro domovský obvod",
                style={"fontWeight": "700", "color": "#334155", "fontSize": "0.9rem",
                       "marginBottom": "0.75rem"}),
        dbc.Row(metric_cards, className="g-2 mb-3"),
        insight_box,

        html.Div([
            html.A(
                dbc.Button([
                    html.I(className="fa-solid fa-map-location-dot", style={"marginRight": "0.4rem"}),
                    f"Prozkoumat {p['district']} detailně"
                ], color="primary", outline=True, size="sm",
                   style={"borderRadius": "0.5rem", "marginTop": "0.75rem"}),
                href=f"/districts/district-detail?district={p['district']}",
                style={"textDecoration": "none"}
            ),
            html.A(
                dbc.Button([
                    html.I(className="fa-solid fa-book-open", style={"marginRight": "0.4rem"}),
                    "Zobrazit teorii"
                ], color="secondary", outline=True, size="sm",
                   style={"borderRadius": "0.5rem", "marginTop": "0.75rem", "marginLeft": "0.5rem"}),
                href="/theory",
                style={"textDecoration": "none"}
            )
        ])
    ])


def layout(persona=None):
    """Generate the personas page layout.

    Args:
        persona: Selected persona ID ('jan', 'elena', 'novak'). URL query param.
    """
    selector_row = dbc.Row([
        dbc.Col(_persona_selector_card("jan", persona == "jan"), md=4, className="mb-3"),
        dbc.Col(_persona_selector_card("elena", persona == "elena"), md=4, className="mb-3"),
        dbc.Col(_persona_selector_card("novak", persona == "novak"), md=4, className="mb-3"),
    ], className="mb-4")

    if persona and persona in PERSONAS:
        detail = _build_persona_detail(persona)
        detail_section = dbc.Card(
            dbc.CardBody(detail),
            className="shadow-sm",
            style={"border": f"1px solid {PERSONAS[persona]['border']}",
                   "borderRadius": "1rem", "background": PERSONAS[persona]["bg"]}
        )
    else:
        detail_section = dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.I(className="fa-solid fa-hand-pointer",
                           style={"fontSize": "2.5rem", "color": "#cbd5e1", "marginBottom": "0.75rem"}),
                    html.P("Vyberte personu výše pro zobrazení dat jejího domovského obvodu.",
                           style={"color": "#94a3b8", "fontSize": "1rem"}),
                ], className="text-center py-4")
            ]),
            className="shadow-sm",
            style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"}
        )

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                page_title(
                    "Persony",
                    align="center",
                    description=(
                        "Stejné město — různé potřeby. Přístup zdola-nahoru (bottom-up): "
                        "jak totéž prostředí ovlivňuje různé obyvatele."
                    ),
                    use_gradient=True
                ),
                selector_row,
                detail_section,
            ], width=12)
        ])
    ], fluid=True, className="py-2")
