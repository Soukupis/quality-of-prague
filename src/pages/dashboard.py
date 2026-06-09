"""Dashboard — Prague Quality of Life overview and metric comparison.

Redesigned as a proper home screen for the QoL application. Answers the
question "What is the state of Quality of Life across Prague right now?"
at a glance, through three visual layers:

1. KPI strip — top/bottom district, city median, district count
2. QoL choropleth map + Top/Bottom 5 ranking
3. Domain averages strip (citywide Safety / Mobility / Accessibility / Environment)

Below is the retained "Porovnat metriku" section — the original bar chart
comparison tool, repositioned as a secondary drill-down.

Theory reference: OECD Better Life Index composite approach; Stiglitz-Sen-
Fitoussi spatial equity; Marans (2012) top-down synthesis.
"""
import json

import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import register_page, dcc, html, callback, Input, Output, exceptions

from src.components.pages.dashboard import district_select, data_select
from src.components.ui import page_title
from src.configs.data_config import DATA_PATHS
from src.utils.loaders.data_loader import read_file
from src.utils.qol_scoring import (
    get_all_scores, composite_score,
    DOMAIN_LABELS, DOMAIN_COLORS, DOMAIN_ICONS,
)

register_page(__name__, path="/dashboard", name="Dashboard")

NORMALIZATION_OPTIONS = [
    {"label": "Počet objektů", "value": "count"},
    {"label": "Hustota (/ km²)", "value": "density"},
]


# ── Data helpers ──────────────────────────────────────────────────────────────

def _city_stats(all_scores):
    """Compute city-wide summary statistics from district QoL scores."""
    composites = {d: composite_score(s) for d, s in all_scores.items()}
    ranked = sorted(composites.items(), key=lambda x: x[1], reverse=True)
    scores_sorted = sorted(composites.values())
    n = len(scores_sorted)
    median = scores_sorted[n // 2]
    domain_avgs = [
        round(sum(s[i] for s in all_scores.values()) / len(all_scores), 1)
        for i in range(4)
    ]
    return {
        "top": ranked[0],
        "bottom": ranked[-1],
        "median": round(median, 1),
        "n_districts": len(all_scores),
        "domain_avgs": domain_avgs,
    }


# ── Map ───────────────────────────────────────────────────────────────────────

def _create_qol_map(all_scores):
    """Choropleth map of Prague colored by composite QoL score."""
    gdf = read_file(DATA_PATHS.get_path("prague_districts"))
    gdf = gdf.to_crs(4326)
    gdf["nazev_1"] = gdf["nazev_1"].fillna("Unknown").astype(str).str.strip()
    geojson = json.loads(gdf[["nazev_1", "geometry"]].to_json())

    districts, scores = [], []
    for feature in geojson["features"]:
        name = feature["properties"]["nazev_1"]
        districts.append(name)
        scores.append(composite_score(all_scores.get(name, [0, 0, 0, 0])))

    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson,
        locations=districts,
        z=scores,
        featureidkey="properties.nazev_1",
        colorscale=[
            [0.00, "#ef4444"],
            [0.40, "#f59e0b"],
            [0.70, "#22c55e"],
            [1.00, "#15803d"],
        ],
        zmin=0,
        zmax=100,
        marker_opacity=0.82,
        marker_line_width=1.5,
        marker_line_color="white",
        colorbar=dict(
            title=dict(text="QoL skóre", font=dict(size=11, color="#475569")),
            thickness=12,
            len=0.65,
            tickfont=dict(size=10, color="#64748b"),
            tickvals=[0, 25, 50, 75, 100],
            x=1.0,
        ),
        hovertemplate=(
            "<b>%{location}</b><br>"
            "QoL composite: <b>%{z:.1f}/100</b><br>"
            "<i style='color:#94a3b8'>Kliknutím zobrazíte detail obvodu</i>"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=9.6,
        mapbox_center={"lat": 50.058, "lon": 14.437},
        margin=dict(l=0, r=0, t=0, b=0),
        height=460,
        paper_bgcolor="white",
    )
    return fig


# ── UI components ─────────────────────────────────────────────────────────────

def _kpi_card(icon_class, label, value, subtitle, color, href=None):
    card = dbc.Card(
        dbc.CardBody(
            html.Div([
                html.I(className=f"fa-solid {icon_class}",
                       style={"fontSize": "1.6rem", "color": color, "minWidth": "2rem"}),
                html.Div([
                    html.Div(label, style={"fontSize": "0.75rem", "color": "#64748b",
                                           "fontWeight": "600", "lineHeight": "1.2",
                                           "textTransform": "uppercase", "letterSpacing": "0.04em"}),
                    html.Div(str(value), style={"fontSize": "1.55rem", "fontWeight": "800",
                                                "color": "#1e293b", "lineHeight": "1.2"}),
                    html.Div(subtitle, style={"fontSize": "0.73rem", "color": "#94a3b8",
                                              "marginTop": "0.1rem"}),
                ], style={"marginLeft": "0.75rem"})
            ], className="d-flex align-items-center")
        ),
        className="shadow-sm h-100",
        style={
            "border": "none",
            "borderRadius": "0.75rem",
            "background": f"linear-gradient(135deg, {color}14 0%, white 100%)",
        }
    )
    if href:
        return html.A(card, href=href, style={"textDecoration": "none", "display": "block", "height": "100%"})
    return card


def _ranking_row(rank, district, score):
    color = "#22c55e" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
    return html.A(
        html.Div([
            html.Span(f"{rank}.",
                      style={"fontSize": "0.75rem", "color": "#94a3b8",
                             "minWidth": "1.4rem", "fontWeight": "600"}),
            html.Span(district,
                      style={"fontSize": "0.82rem", "fontWeight": "600", "color": "#1e293b",
                             "flex": "1", "marginLeft": "0.3rem",
                             "overflow": "hidden", "textOverflow": "ellipsis", "whiteSpace": "nowrap"}),
            html.Div(
                html.Div(style={
                    "width": f"{score}%", "background": color,
                    "height": "5px", "borderRadius": "3px",
                }),
                style={"width": "55px", "background": "#f1f5f9",
                       "borderRadius": "3px", "marginLeft": "0.5rem", "flexShrink": "0"}
            ),
            html.Span(f"{score:.0f}",
                      style={"fontSize": "0.82rem", "fontWeight": "700", "color": color,
                             "minWidth": "1.8rem", "textAlign": "right", "marginLeft": "0.3rem"}),
        ], className="d-flex align-items-center",
           style={"padding": "0.4rem 0.25rem", "borderBottom": "1px solid #f1f5f9",
                  "transition": "background 0.15s"}),
        href=f"/districts/district-detail?district={district}",
        style={"textDecoration": "none"}
    )


def _ranking_panel(all_scores, n=5):
    ranked = sorted(
        [(d, composite_score(s)) for d, s in all_scores.items()],
        key=lambda x: x[1], reverse=True
    )
    top = ranked[:n]
    bottom = list(reversed(ranked[-n:]))

    return html.Div([
        html.Div([
            html.I(className="fa-solid fa-trophy",
                   style={"color": "#22c55e", "fontSize": "0.9rem", "marginRight": "0.4rem"}),
            html.Span("Nejlepší obvody",
                      style={"fontWeight": "700", "color": "#22c55e",
                             "fontSize": "0.82rem", "textTransform": "uppercase",
                             "letterSpacing": "0.04em"}),
        ], className="d-flex align-items-center mb-1"),
        *[_ranking_row(i + 1, d, s) for i, (d, s) in enumerate(top)],

        html.Hr(style={"margin": "0.75rem 0", "borderColor": "#e2e8f0"}),

        html.Div([
            html.I(className="fa-solid fa-arrow-trend-down",
                   style={"color": "#ef4444", "fontSize": "0.9rem", "marginRight": "0.4rem"}),
            html.Span("Nejslabší obvody",
                      style={"fontWeight": "700", "color": "#ef4444",
                             "fontSize": "0.82rem", "textTransform": "uppercase",
                             "letterSpacing": "0.04em"}),
        ], className="d-flex align-items-center mb-1"),
        *[_ranking_row(len(all_scores) - n + i + 1, d, s) for i, (d, s) in enumerate(bottom)],

        html.Div([
            html.A("Zobrazit celé pořadí →",
                   href="/qol-index",
                   style={"fontSize": "0.78rem", "color": "#667eea",
                          "textDecoration": "none", "fontWeight": "600"})
        ], className="mt-3 text-end"),
    ])


def _domain_avg_card(label, avg, color, icon_class):
    return dbc.Card(
        dbc.CardBody(
            html.Div([
                html.I(className=f"fa-solid {icon_class}",
                       style={"fontSize": "1.3rem", "color": color, "minWidth": "1.6rem"}),
                html.Div([
                    html.Div(label,
                             style={"fontSize": "0.73rem", "color": "#64748b", "fontWeight": "600",
                                    "textTransform": "uppercase", "letterSpacing": "0.04em",
                                    "lineHeight": "1.2"}),
                    html.Div(f"{avg:.1f}",
                             style={"fontSize": "1.35rem", "fontWeight": "800",
                                    "color": "#1e293b", "lineHeight": "1.3"}),
                    html.Div("/100 průměr Prahy",
                             style={"fontSize": "0.7rem", "color": "#94a3b8"}),
                    html.Div(
                        html.Div(style={
                            "width": f"{avg}%", "background": color,
                            "height": "4px", "borderRadius": "2px",
                        }),
                        style={"width": "100%", "background": "#f1f5f9",
                               "borderRadius": "2px", "marginTop": "0.4rem"}
                    ),
                ], style={"marginLeft": "0.6rem", "flex": "1"})
            ], className="d-flex align-items-start")
        ),
        className="shadow-sm h-100",
        style={"border": "none", "borderRadius": "0.75rem",
               "background": f"linear-gradient(135deg, {color}10 0%, white 100%)"}
    )


# ── Layout ────────────────────────────────────────────────────────────────────

def layout():
    """Generate the dashboard layout with live QoL data."""
    all_scores = get_all_scores()
    stats = _city_stats(all_scores)
    top_name, top_score = stats["top"]
    bot_name, bot_score = stats["bottom"]

    return dbc.Container([
        dcc.Location(id="dashboard-url", refresh=True),

        # ── Title ──
        dbc.Row([
            dbc.Col(page_title(
                "Dashboard",
                align="center",
                description=(
                    "Přehled kvality života napříč pražskými obvody. "
                    "Kliknutím na obvod v mapě nebo v žebříčku zobrazíte jeho detail."
                ),
                use_gradient=True
            ), width=12)
        ]),

        # ── KPI strip ──
        dbc.Row([
            dbc.Col(_kpi_card(
                "fa-ranking-star", "Nejlepší obvod",
                f"{top_name}",
                f"{top_score:.1f}/100 composite skóre",
                "#22c55e",
                href=f"/districts/district-detail?district={top_name}",
            ), xs=6, md=3, className="mb-3"),
            dbc.Col(_kpi_card(
                "fa-chart-simple", "Medián QoL",
                f"{stats['median']:.1f}/100",
                "střed distribuce všech obvodů",
                "#667eea",
            ), xs=6, md=3, className="mb-3"),
            dbc.Col(_kpi_card(
                "fa-arrow-trend-down", "Nejslabší obvod",
                f"{bot_name}",
                f"{bot_score:.1f}/100 composite skóre",
                "#ef4444",
                href=f"/districts/district-detail?district={bot_name}",
            ), xs=6, md=3, className="mb-3"),
            dbc.Col(_kpi_card(
                "fa-city", "Obvodů v analýze",
                str(stats["n_districts"]),
                "ze 57 městských částí Prahy",
                "#0ea5e9",
            ), xs=6, md=3, className="mb-3"),
        ], className="mb-3"),

        # ── QoL map + Rankings ──
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.Div([
                        html.I(className="fa-solid fa-map me-2",
                               style={"color": "#667eea"}),
                        html.Span("QoL mapa Prahy",
                                  style={"fontWeight": "700", "fontSize": "1rem"}),
                        html.Span(" — kliknutím na obvod zobrazíte detail",
                                  style={"fontSize": "0.82rem", "color": "#94a3b8",
                                         "marginLeft": "0.4rem"}),
                    ], className="d-flex align-items-center")),
                    dbc.CardBody(
                        dcc.Graph(
                            id="dashboard-qol-map",
                            figure=_create_qol_map(all_scores),
                            config={"displayModeBar": False, "scrollZoom": False},
                            style={"height": "460px"},
                        ),
                        style={"padding": "0.5rem"},
                    ),
                ], className="shadow-sm h-100",
                   style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"}),
                md=8, className="mb-4"
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.Div([
                        html.I(className="fa-solid fa-list-ol me-2",
                               style={"color": "#f59e0b"}),
                        html.Span("Žebříček obvodů",
                                  style={"fontWeight": "700", "fontSize": "1rem"}),
                    ], className="d-flex align-items-center")),
                    dbc.CardBody(
                        _ranking_panel(all_scores, n=5),
                        style={"overflowY": "auto", "maxHeight": "460px"},
                    ),
                ], className="shadow-sm h-100",
                   style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"}),
                md=4, className="mb-4"
            ),
        ]),

        # ── Domain averages ──
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Div([
                        html.I(className="fa-solid fa-layer-group me-2",
                               style={"color": "#475569", "fontSize": "0.9rem"}),
                        html.Span("Průměrné skóre domén napříč Prahou",
                                  style={"fontWeight": "700", "fontSize": "0.9rem",
                                         "color": "#334155"}),
                    ], className="d-flex align-items-center mb-3"),
                    dbc.Row([
                        dbc.Col(
                            _domain_avg_card(
                                DOMAIN_LABELS[i],
                                stats["domain_avgs"][i],
                                DOMAIN_COLORS[i],
                                DOMAIN_ICONS[i],
                            ),
                            xs=6, md=3, className="mb-3"
                        )
                        for i in range(4)
                    ], className="g-2"),
                ]),
                width=12
            )
        ], className="mb-2"),

        # ── Compare section ──
        html.Hr(style={"borderColor": "#e2e8f0", "margin": "1.5rem 0"}),

        dbc.Row([
            dbc.Col(html.Div([
                html.I(className="fa-solid fa-chart-bar me-2",
                       style={"color": "#667eea", "fontSize": "1.1rem"}),
                html.Span("Porovnat metriku",
                          style={"fontWeight": "700", "fontSize": "1.1rem", "color": "#1e293b"}),
                html.Span(" — vyberte obvody a kategorii dat k podrobnému porovnání",
                          style={"fontSize": "0.85rem", "color": "#94a3b8", "marginLeft": "0.5rem"}),
            ], className="d-flex align-items-center"), width=12)
        ], className="mb-3"),

        dbc.Row([
            dbc.Col(district_select(), width=6, className="mb-3"),
            dbc.Col(data_select(), width=6, className="mb-3"),
        ]),

        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody(
                        html.Div([
                            html.I(className="fa-solid fa-sliders",
                                   style={"fontSize": "1rem", "color": "#667eea",
                                          "marginRight": "0.5rem"}),
                            html.Span("Zobrazení:", className="fw-bold me-3",
                                      style={"color": "#2c3e50", "fontSize": "0.95rem"}),
                            dcc.RadioItems(
                                id="normalization-mode",
                                options=NORMALIZATION_OPTIONS,
                                value="count",
                                inline=True,
                                inputStyle={"marginRight": "0.3rem", "cursor": "pointer"},
                                labelStyle={"marginRight": "1.5rem", "cursor": "pointer",
                                            "fontSize": "0.95rem", "color": "#475569"},
                            ),
                        ], className="d-flex align-items-center"),
                    )
                ], className="shadow-sm",
                   style={"border": "none", "borderRadius": "1rem",
                          "background": "linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%)"}),
                width=12, className="mb-3"
            )
        ]),

        dbc.Row([
            dbc.Col(
                dbc.Card(dcc.Loading(
                    id="loading_bar_chart",
                    type="circle",
                    children=html.Div(id="bar_chart_container"),
                    color="#3b82f6",
                    fullscreen=False,
                    style={"minHeight": "400px"},
                    overlay_style={"visibility": "visible", "opacity": 0.5},
                )),
            ),
            dbc.Col(
                dbc.Card(dcc.Loading(
                    id="loading_district_map",
                    type="circle",
                    children=html.Div(id="district_map_container"),
                    color="#3b82f6",
                    fullscreen=False,
                    style={"minHeight": "400px"},
                    overlay_style={"visibility": "visible", "opacity": 0.5},
                )),
            ),
        ]),

    ], fluid=True, className="py-3")


# ── Callback: map click → district detail ────────────────────────────────────

@callback(
    Output("dashboard-url", "href"),
    Input("dashboard-qol-map", "clickData"),
    prevent_initial_call=True,
)
def navigate_from_qol_map(click_data):
    if not click_data:
        raise exceptions.PreventUpdate
    district = click_data["points"][0]["location"]
    return f"/districts/district-detail?district={district}"
