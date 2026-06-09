import dash_bootstrap_components as dbc
from dash import register_page, html, dcc, callback, Input, Output, State, ctx

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
from src.i18n import t

register_page(__name__, path="/personas", name="Persony")

PERSONAS = {
    "jan": {
        "id": "jan",
        "name": "Jan",
        "age": 75,
        "district": "Praha 7",
        "neighborhood": "Holešovice",
        "desc_key": "persona_jan_desc",
        "age_loc_key": "persona_jan_age_loc",
        "icon": "fa-person-cane",
        "color": "#0f766e",
        "bg": "#f0fdfa",
        "border": "#d1fae5",
        "concerns": [
            ("fa-elevator",       "concern_elevator_title", "concern_elevator_sub"),
            ("fa-wheelchair",     "concern_ztp_title",      "concern_ztp_sub"),
            ("fa-shield-halved",  "concern_safety_title",   "concern_safety_sub"),
            ("fa-train-subway",   "concern_metro_title",    "concern_metro_sub"),
        ],
        "relevant_metrics": ["subway_entrances", "ztp_parking", "police_stations"],
    },
    "elena": {
        "id": "elena",
        "name": "Elena",
        "age": 28,
        "district": "Praha 8",
        "neighborhood": "Karlín",
        "desc_key": "persona_elena_desc",
        "age_loc_key": "persona_elena_age_loc",
        "icon": "fa-person-biking",
        "color": "#1d4ed8",
        "bg": "#eff6ff",
        "border": "#dbeafe",
        "concerns": [
            ("fa-train-subway", "concern_metro_title",          "concern_metro_sub"),
            ("fa-car-side",     "concern_pr_title",             "concern_pr_sub"),
            ("fa-parking",      "concern_parking_meters_title", "concern_parking_meters_sub"),
            ("fa-shield-halved","concern_safety2_title",        "concern_safety2_sub"),
        ],
        "relevant_metrics": ["subway_entrances", "parking_meters", "police_stations"],
    },
    "novak": {
        "id": "novak",
        "name": "Rodina Novákových",
        "age": None,
        "district": "Praha 6",
        "neighborhood": "Dejvice",
        "desc_key": "persona_novak_desc",
        "age_loc_key": "persona_novak_age_loc",
        "icon": "fa-people-roof",
        "color": "#b45309",
        "bg": "#fffbeb",
        "border": "#fde68a",
        "concerns": [
            ("fa-shield-halved", "concern_safety2_title",  "concern_safety2_sub"),
            ("fa-wheelchair",    "concern_stroller_title", "concern_stroller_sub"),
            ("fa-train-subway",  "concern_metro2_title",   "concern_metro2_sub"),
            ("fa-wind",          "concern_air_title",      "concern_air_sub"),
        ],
        "relevant_metrics": ["police_stations", "subway_entrances", "ztp_parking"],
    }
}

_NORMAL_CARD_STYLE = {
    "border": "2px solid #e2e8f0",
    "background": "white",
    "cursor": "pointer",
    "borderRadius": "1rem",
    "transition": "all 0.2s ease",
}


def _selected_card_style(persona_id):
    p = PERSONAS[persona_id]
    return {
        "border": f"2px solid {p['color']}",
        "background": p["bg"],
        "cursor": "pointer",
        "borderRadius": "1rem",
        "transition": "all 0.2s ease",
    }


def _persona_selector_card(persona, lang):
    p = PERSONAS[persona]
    return html.Div(
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.I(className=f"fa-solid {p['icon']}",
                           style={"fontSize": "2rem", "color": p["color"],
                                  "marginRight": "0.75rem"}),
                    html.Div([
                        html.Div(p["name"], style={"fontWeight": "700", "fontSize": "1rem",
                                                   "color": "#1e293b"}),
                        html.Div(t(p["age_loc_key"], lang),
                                 style={"fontSize": "0.8rem", "color": "#64748b"}),
                    ])
                ], className="d-flex align-items-center mb-2"),
                html.P(t(p["desc_key"], lang),
                       style={"fontSize": "0.8rem", "color": "#475569",
                              "lineHeight": "1.4", "marginBottom": 0})
            ])
        ], className="shadow-sm h-100", style={"border": "none", "borderRadius": "1rem"}),
        id=f"persona-card-{persona}",
        n_clicks=0,
        style=_NORMAL_CARD_STYLE
    )


def _concern_row(icon_class, title_key, sub_key, color, lang):
    return html.Div([
        html.I(className=f"fa-solid {icon_class}",
               style={"fontSize": "1.1rem", "color": color, "minWidth": "1.5rem"}),
        html.Div([
            html.Span(t(title_key, lang),
                      style={"fontWeight": "600", "fontSize": "0.85rem", "color": "#1e293b"}),
            html.Span(f" — {t(sub_key, lang)}",
                      style={"fontSize": "0.82rem", "color": "#64748b"}),
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


def _build_persona_detail(persona_id, lang):
    if persona_id not in PERSONAS:
        return None

    p = PERSONAS[persona_id]
    polygons = get_district_polygons()
    district = p["district"]

    if district not in polygons:
        return html.P(t("district_no_data", lang, district=district))

    polygon = polygons[district]
    areas = get_district_areas_km2()
    area_km2 = areas.get(district, 1.0)

    metro_stats = _get_metro_accessibility_stats(polygon)
    ztp_stats = _get_ztp_stats(district, polygon)
    police_count = len(get_points_in_district(district, "police_stations"))
    metro_count = metro_stats["total"]

    metric_cards = []

    if persona_id == "jan":
        metric_cards = [
            dbc.Col(_metric_card("fa-train-subway",
                                  t("metric_subway_label", lang), metro_count,
                                  t("metric_subway_sub", lang, district=district),
                                  p["color"]),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-elevator",
                                  t("metric_elevator_label", lang),
                                  f"{metro_stats['elevator']} ({metro_stats['lift_ratio']}%)",
                                  t("metric_elevator_sub", lang), "#059669"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-wheelchair",
                                  t("metric_ztp_label", lang), ztp_stats["total_spaces"],
                                  t("metric_ztp_sub", lang, density=f"{ztp_stats['density_per_km2']:.1f}"),
                                  "#7c3aed"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-building-shield",
                                  t("metric_police_label", lang), police_count,
                                  t("metric_police_sub", lang, rate=round(police_count / area_km2, 2)),
                                  "#dc2626"),
                    xs=6, sm=4, md=3, className="mb-3"),
        ]
        insight = t("persona_insight_jan", lang,
                    neighborhood=p["neighborhood"], district=district,
                    metro_count=metro_count,
                    lift_ratio=metro_stats["lift_ratio"],
                    stairs_only=metro_stats["stairs_only"])

    elif persona_id == "elena":
        parking_count = len(get_points_in_district(district, "parking_meters"))
        pr_stats = _get_pr_stats(polygon, lang)
        pr_count = pr_stats["count"] if pr_stats else 0
        pr_capacity = pr_stats["current_capacity"] if pr_stats else 0
        lines_str = ", ".join([f"{l}" for l, c in metro_stats["line_counts"].items() if c > 0])
        metric_cards = [
            dbc.Col(_metric_card("fa-train-subway",
                                  t("metric_subway_label", lang), metro_count,
                                  t("metric_lines", lang, lines=lines_str),
                                  p["color"]),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-car-side",
                                  t("metric_pr_label", lang), pr_count,
                                  t("metric_pr_capacity", lang, cap=pr_capacity) if pr_capacity
                                  else t("metric_pr_none", lang),
                                  "#0f766e"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-parking",
                                  t("metric_meters_label", lang), parking_count,
                                  t("metric_meters_sub", lang, rate=round(parking_count / area_km2, 1)),
                                  "#8B008B"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-building-shield",
                                  t("metric_police_label", lang), police_count,
                                  t("metric_police_sub", lang, rate=round(police_count / area_km2, 2)),
                                  "#dc2626"),
                    xs=6, sm=4, md=3, className="mb-3"),
        ]
        insight = t("persona_insight_elena", lang,
                    neighborhood=p["neighborhood"], district=district,
                    metro_count=metro_count, lines=lines_str,
                    meter_density=f"{round(parking_count / area_km2, 1):.1f}")

    else:  # novak
        metric_cards = [
            dbc.Col(_metric_card("fa-building-shield",
                                  t("metric_police_label", lang), police_count,
                                  t("metric_police_sub", lang, rate=round(police_count / area_km2, 2)),
                                  p["color"]),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-train-subway",
                                  t("metric_subway_label", lang), metro_count,
                                  t("metric_subway_sub", lang, district=district),
                                  "#1d4ed8"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-wheelchair",
                                  t("metric_ztp_label", lang), ztp_stats["total_spaces"],
                                  t("metric_ztp_sub", lang, density=f"{ztp_stats['density_per_km2']:.1f}"),
                                  "#7c3aed"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_metric_card("fa-elevator",
                                  t("metric_metro_stroller", lang),
                                  f"{metro_stats['elevator']} ({metro_stats['lift_ratio']}%)",
                                  t("metric_stroller_sub", lang),
                                  "#059669"),
                    xs=6, sm=4, md=3, className="mb-3"),
        ]
        insight = t("persona_insight_novak", lang,
                    neighborhood=p["neighborhood"], district=district,
                    lift_ratio=metro_stats["lift_ratio"])

    lang_suffix = f"?lang={lang}" if lang != "cs" else ""

    concerns_section = html.Div([
        html.H6(t("persona_concerns_title", lang),
                style={"fontWeight": "700", "color": "#334155",
                       "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
        *[_concern_row(icon, title_key, sub_key, p["color"], lang)
          for icon, title_key, sub_key in p["concerns"]]
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
                html.H3(p["name"], style={"fontWeight": "800", "color": "#1e293b",
                                          "marginBottom": "0.1rem"}),
                html.Span(t(p["age_loc_key"], lang),
                          style={"fontSize": "0.95rem", "color": "#64748b"}),
            ])
        ], className="d-flex align-items-center mb-3",
           style={"borderBottom": f"3px solid {p['color']}", "paddingBottom": "0.75rem"}),

        html.P(t(p["desc_key"], lang),
               style={"fontSize": "0.95rem", "color": "#475569",
                      "lineHeight": "1.6", "marginBottom": "1rem"}),
        concerns_section,

        html.H6(t("persona_district_data_title", lang),
                style={"fontWeight": "700", "color": "#334155", "fontSize": "0.9rem",
                       "marginBottom": "0.75rem"}),
        dbc.Row(metric_cards, className="g-2 mb-3"),
        insight_box,

        html.Div([
            html.A(
                dbc.Button([
                    html.I(className="fa-solid fa-map-location-dot", style={"marginRight": "0.4rem"}),
                    t("persona_explore_btn", lang, district=p["district"])
                ], color="primary", outline=True, size="sm",
                   style={"borderRadius": "0.5rem", "marginTop": "0.75rem"}),
                href=f"/districts/district-detail?district={p['district']}{lang_suffix}",
                style={"textDecoration": "none"}
            ),
            html.A(
                dbc.Button([
                    html.I(className="fa-solid fa-book-open", style={"marginRight": "0.4rem"}),
                    t("persona_theory_btn", lang)
                ], color="secondary", outline=True, size="sm",
                   style={"borderRadius": "0.5rem", "marginTop": "0.75rem", "marginLeft": "0.5rem"}),
                href=f"/theory{lang_suffix}",
                style={"textDecoration": "none"}
            )
        ])
    ])


def _detail_card(persona_id, lang):
    if persona_id and persona_id in PERSONAS:
        p = PERSONAS[persona_id]
        return dbc.Card(
            dbc.CardBody(_build_persona_detail(persona_id, lang)),
            className="shadow-sm",
            style={"border": f"1px solid {p['border']}",
                   "borderRadius": "1rem", "background": p["bg"]}
        )
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                html.I(className="fa-solid fa-hand-pointer",
                       style={"fontSize": "2.5rem", "color": "#cbd5e1", "marginBottom": "0.75rem"}),
                html.P(t("persona_select_placeholder", lang),
                       style={"color": "#94a3b8", "fontSize": "1rem"}),
            ], className="text-center py-4")
        ]),
        className="shadow-sm",
        style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"}
    )


def layout(persona=None, lang="cs"):
    return dbc.Container([
        dcc.Store(id='selected-persona-store', data=persona),
        dbc.Row([
            dbc.Col([
                page_title(
                    t("personas_title", lang),
                    align="center",
                    description=t("personas_desc", lang),
                    use_gradient=True
                ),
                dbc.Row([
                    dbc.Col(_persona_selector_card("jan", lang), md=4, className="mb-3"),
                    dbc.Col(_persona_selector_card("elena", lang), md=4, className="mb-3"),
                    dbc.Col(_persona_selector_card("novak", lang), md=4, className="mb-3"),
                ], className="mb-4"),
                html.Div(id='persona-detail-container'),
            ], width=12)
        ])
    ], fluid=True, className="py-2")


# ── Callbacks ─────────────────────────────────────────────────────────────────

@callback(
    Output('selected-persona-store', 'data'),
    Input('persona-card-jan', 'n_clicks'),
    Input('persona-card-elena', 'n_clicks'),
    Input('persona-card-novak', 'n_clicks'),
    prevent_initial_call=True,
)
def select_persona(jan_n, elena_n, novak_n):
    if ctx.triggered_id is None:
        return None
    return ctx.triggered_id.replace('persona-card-', '')


@callback(
    Output('persona-detail-container', 'children'),
    Output('persona-card-jan', 'style'),
    Output('persona-card-elena', 'style'),
    Output('persona-card-novak', 'style'),
    Input('selected-persona-store', 'data'),
    State('lang-store', 'data'),
)
def render_persona(persona_id, lang):
    lang = lang or "cs"

    def card_style(pid):
        return _selected_card_style(pid) if pid == persona_id else _NORMAL_CARD_STYLE

    return (
        _detail_card(persona_id, lang),
        card_style('jan'),
        card_style('elena'),
        card_style('novak'),
    )
