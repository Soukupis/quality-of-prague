"""QoL Composite Index page — radar chart and district ranking.

Operationalizes the OECD Better Life Index approach: normalize multiple
indicators across QOUL domains, weight them, and produce a composite score
per district. Follows Marans' top-down synthesis approach.

Domains scored (0–100 per domain):
  - Socioekonomická bezpečnost (30%): police station density
  - Mobilita (37%): metro entrance density + elevator accessibility ratio
  - Přístupnost (23%): ZTP parking density + metro elevator ratio
  - Prostředí (10%): park density (OSM leisure=park per km²)

Theory reference: OECD Better Life Index normalization; Stiglitz-Sen-Fitoussi;
Marans (2012) dual-methodological QOUL framework.
"""
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import register_page, html, dcc, callback, Input, Output, exceptions

from src.components.ui import page_title
from src.utils.qol_scoring import (
    get_all_scores, compute_raw_scores, compute_domain_scores,
    composite_score as _composite_score,
    DOMAIN_LABELS, DOMAIN_COLORS,
)

register_page(__name__, path="/qol-index", name="QoL Index")


def _create_radar_chart(district, domain_scores):
    """Create a radar chart for one district."""
    p = PERSONAS_CONTEXT = DOMAIN_LABELS
    values = domain_scores + [domain_scores[0]]   # close the polygon
    labels = DOMAIN_LABELS + [DOMAIN_LABELS[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.25)',
        line=dict(color='#667eea', width=2),
        name=district,
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100],
                            tickfont=dict(size=10, color="#94a3b8"),
                            gridcolor="#e2e8f0"),
            angularaxis=dict(tickfont=dict(size=11, color="#334155")),
            bgcolor="white",
        ),
        showlegend=False,
        paper_bgcolor="white",
        margin=dict(l=60, r=60, t=40, b=40),
        height=340,
    )
    return fig


def _create_ranking_chart(all_scores):
    """Create a horizontal bar chart ranking all districts by composite score."""
    items = sorted(all_scores.items(), key=lambda x: _composite_score(x[1]), reverse=True)
    districts = [d for d, _ in items]
    scores = [_composite_score(s) for _, s in items]
    colors = [
        '#22c55e' if s >= 70 else '#f59e0b' if s >= 40 else '#ef4444'
        for s in scores
    ]

    fig = go.Figure(go.Bar(
        x=scores,
        y=districts,
        orientation='h',
        marker=dict(color=colors, line=dict(color='white', width=0)),
        text=[f"{s:.1f}" for s in scores],
        textposition='outside',
        textfont=dict(size=11, color='#1e293b'),
        hovertemplate='<b>%{y}</b><br>QoL skóre: <b>%{x:.1f}/100</b><br><i>Kliknutím vyberte obvod</i><extra></extra>',
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 115], showgrid=True, gridcolor='#f1f5f9',
                   title_text="Composite QoL skóre (0–100)"),
        yaxis=dict(autorange='reversed', tickfont=dict(size=12)),
        paper_bgcolor='white',
        plot_bgcolor='#fafafa',
        margin=dict(l=150, r=60, t=20, b=40),
        height=max(500, len(districts) * 26 + 80),
        bargap=0.3,
        uniformtext=dict(mode='hide', minsize=8),
    )
    return fig


def layout():
    """Generate the QoL index page layout."""
    all_scores = get_all_scores()

    district_options = sorted([{"label": d, "value": d} for d in all_scores.keys()],
                               key=lambda x: x["label"])
    default_district = "Praha 1"

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                page_title(
                    "QoL Index",
                    align="center",
                    description=(
                        "Kompozitní skóre kvality života na základě QOUL 4 domén. "
                        "Normalizace min-max dle přístupu OECD Better Life Index. "
                        "Doména Prostředí je aktivní — hustota parků (OSM). PM2.5 a hluk v další fázi."
                    ),
                    use_gradient=True
                ),

                # ── Methodology note ──
                dbc.Alert([
                    html.I(className="fa-solid fa-circle-info me-2"),
                    html.Strong("Metodologie: "),
                    "Každá doména je normalizována na škálu 0–100 metodou min-max (nejlepší "
                    "obvod v Praze = 100, nejhorší = 0). Composite skóre váží Bezpečnost (30%), "
                    "Mobilitu (37%), Přístupnost (23%), Prostředí (10%). Doména Prostředí "
                    "aktuálně obsahuje hustotu parků (OSM, leisure=park) — PM2.5, hluk a "
                    "tepelný ostrov budou přidány v další fázi po integraci dat ČHMÚ."
                ], color="info", className="mb-4",
                   style={"fontSize": "0.88rem", "borderRadius": "0.75rem"}),

                # ── Radar section ──
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.I(className="fa-solid fa-chart-radar me-2",
                                   style={"color": "#667eea"}),
                            html.Span("Radarový diagram — QOUL domény",
                                      style={"fontWeight": "700", "fontSize": "1rem"}),
                        ], className="d-flex align-items-center")
                    ),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Vyberte obvod:", style={"fontWeight": "600",
                                                                     "fontSize": "0.9rem",
                                                                     "color": "#334155"}),
                                dcc.Dropdown(
                                    id="qol-district-dropdown",
                                    options=district_options,
                                    value=default_district,
                                    clearable=False,
                                    className="custom-dropdown",
                                    style={"fontSize": "0.95rem"}
                                ),
                            ], md=4, className="mb-3"),
                            dbc.Col([
                                dcc.Loading(
                                    id="loading-radar",
                                    type="circle",
                                    children=html.Div(id="qol-radar-container"),
                                    color="#667eea",
                                )
                            ], md=8),
                        ]),
                        # Domain score cards
                        html.Div(id="qol-domain-cards"),
                    ])
                ], className="shadow-sm mb-4",
                   style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"}),

                # ── Ranking section ──
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.I(className="fa-solid fa-ranking-star me-2",
                                   style={"color": "#f59e0b"}),
                            html.Span("Pořadí všech obvodů podle QoL Composite skóre",
                                      style={"fontWeight": "700", "fontSize": "1rem"}),
                        ], className="d-flex align-items-center")
                    ),
                    dbc.CardBody([
                        dcc.Graph(
                            id="qol-ranking-chart",
                            figure=_create_ranking_chart(all_scores),
                            config={"displayModeBar": False},
                            style={"height": f"{max(500, len(all_scores) * 26 + 80)}px",
                                   "cursor": "pointer"}
                        )
                    ])
                ], className="shadow-sm mb-4",
                   style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"}),

                # ── Domain descriptions ──
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.I(className="fa-solid fa-list-check me-2",
                                   style={"color": "#0f766e"}),
                            html.Span("Složení domén",
                                      style={"fontWeight": "700", "fontSize": "1rem"}),
                        ], className="d-flex align-items-center")
                    ),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(_domain_card(
                                "fa-shield-halved", "1. Bezpečnost (30%)", "#0f766e",
                                "Hustota policejních stanic / km². Vyšší = lépe.",
                                "Zdroj: Objekty MP Praha"
                            ), md=6, className="mb-3"),
                            dbc.Col(_domain_card(
                                "fa-train-subway", "2. Mobilita (37%)", "#1d4ed8",
                                "70% husota vstupů do metra / km² + 30% podíl vstupů s výtahem.",
                                "Zdroj: Vstupy do metra"
                            ), md=6, className="mb-3"),
                            dbc.Col(_domain_card(
                                "fa-wheelchair", "3. Přístupnost (23%)", "#7c3aed",
                                "60% hustota ZTP parkovacích míst / km² + 40% podíl vstupů s výtahem.",
                                "Zdroj: Parkovací stání ZTP + Vstupy do metra"
                            ), md=6, className="mb-3"),
                            dbc.Col(_domain_card(
                                "fa-tree", "4. Prostředí (10%)", "#16a34a",
                                "Hustota parků (OSM leisure=park) na km². Vyšší hustota = lepší dostupnost zeleně.",
                                "Zdroj: OpenStreetMap / Overpass API — PM2.5 a hluk v Phase 4"
                            ), md=6, className="mb-3"),
                        ])
                    ])
                ], className="shadow-sm",
                   style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"}),

            ], width=12)
        ])
    ], fluid=True, className="py-2")


def _domain_card(icon_class, title, color, description, source):
    return html.Div([
        html.Div([
            html.I(className=f"fa-solid {icon_class}",
                   style={"fontSize": "1.2rem", "color": color, "marginRight": "0.5rem"}),
            html.Span(title, style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#1e293b"}),
        ], className="d-flex align-items-center mb-1"),
        html.P(description, style={"fontSize": "0.82rem", "color": "#475569",
                                    "marginBottom": "0.25rem"}),
        html.Span(source, style={"fontSize": "0.75rem", "color": "#94a3b8", "fontStyle": "italic"}),
    ], style={"background": "#f8fafc", "borderRadius": "0.5rem",
              "padding": "0.6rem 0.75rem", "borderLeft": f"3px solid {color}"})


# ── Callbacks ─────────────────────────────────────────────────────────────────

@callback(
    Output("qol-radar-container", "children"),
    Output("qol-domain-cards", "children"),
    Input("qol-district-dropdown", "value"),
)
def update_radar(district):
    scores = get_all_scores()
    if not district or district not in scores:
        return html.P("Vyberte obvod."), None

    domain_scores = scores[district]
    composite = _composite_score(domain_scores)

    radar_fig = _create_radar_chart(district, domain_scores)

    domain_cards = dbc.Row([
        dbc.Col(_score_card(DOMAIN_LABELS[i], domain_scores[i], DOMAIN_COLORS[i]),
                xs=6, sm=3, className="mb-3")
        for i in range(4)
    ] + [
        dbc.Col(_score_card("Composite", composite, "#667eea", is_composite=True),
                xs=12, sm=12, className="mb-3")
    ], className="g-2 mt-1")

    return dcc.Graph(
        figure=radar_fig,
        config={"displayModeBar": False},
        style={"height": "340px"}
    ), domain_cards


@callback(
    Output("qol-district-dropdown", "value"),
    Input("qol-ranking-chart", "clickData"),
    prevent_initial_call=True,
)
def select_district_from_ranking(click_data):
    if click_data is None:
        raise exceptions.PreventUpdate
    return click_data["points"][0]["y"]


def _score_card(label, score, color, is_composite=False):
    bg = f"linear-gradient(135deg, {color}15 0%, white 100%)" if not is_composite else (
        "linear-gradient(135deg, #667eea20 0%, #764ba215 100%)"
    )
    return dbc.Card(
        dbc.CardBody(html.Div([
            html.Div(label, style={"fontSize": "0.78rem", "color": "#64748b",
                                   "fontWeight": "600", "marginBottom": "0.25rem"}),
            html.Div(f"{score:.1f}", style={
                "fontSize": "1.8rem" if is_composite else "1.5rem",
                "fontWeight": "800",
                "color": color,
                "lineHeight": "1.2"
            }),
            html.Div("/100", style={"fontSize": "0.72rem", "color": "#94a3b8"}),
        ])),
        className="shadow-sm text-center h-100",
        style={"border": f"1px solid {color}30", "borderRadius": "0.75rem",
               "background": bg}
    )
