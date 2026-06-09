"""QoL Composite Index page — radar chart and district ranking."""
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import register_page, html, dcc, callback, Input, Output, State, exceptions

from src.components.ui import page_title
from src.utils.qol_scoring import (
    get_all_scores,
    composite_score as _composite_score,
    DOMAIN_LABEL_KEYS, DOMAIN_COLORS,
)
from src.i18n import t

register_page(__name__, path="/qol-index", name="QoL Index")


def _create_radar_chart(district, domain_scores, lang):
    domain_labels = [t(k, lang) for k in DOMAIN_LABEL_KEYS]
    values = domain_scores + [domain_scores[0]]
    labels = domain_labels + [domain_labels[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values, theta=labels,
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


def _create_ranking_chart(all_scores, lang):
    items = sorted(all_scores.items(), key=lambda x: _composite_score(x[1]), reverse=True)
    districts = [d for d, _ in items]
    scores = [_composite_score(s) for _, s in items]
    colors = [
        '#22c55e' if s >= 70 else '#f59e0b' if s >= 40 else '#ef4444'
        for s in scores
    ]
    hover_template = t("qol_ranking_hover", lang).replace("%{{", "%{").replace("}}", "}")

    fig = go.Figure(go.Bar(
        x=scores, y=districts,
        orientation='h',
        marker=dict(color=colors, line=dict(color='white', width=0)),
        text=[f"{s:.1f}" for s in scores],
        textposition='outside',
        textfont=dict(size=11, color='#1e293b'),
        hovertemplate=f'<b>%{{y}}</b><br>{t("qol_ranking_hover", lang)}<extra></extra>',
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 115], showgrid=True, gridcolor='#f1f5f9',
                   title_text=t("qol_axis_label", lang)),
        yaxis=dict(autorange='reversed', tickfont=dict(size=12)),
        paper_bgcolor='white',
        plot_bgcolor='#fafafa',
        margin=dict(l=150, r=60, t=20, b=40),
        height=max(500, len(districts) * 26 + 80),
        bargap=0.3,
        uniformtext=dict(mode='hide', minsize=8),
    )
    return fig


def _domain_card(icon_class, title, color, description, source):
    return html.Div([
        html.Div([
            html.I(className=f"fa-solid {icon_class}",
                   style={"fontSize": "1.2rem", "color": color, "marginRight": "0.5rem"}),
            html.Span(title, style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#1e293b"}),
        ], className="d-flex align-items-center mb-1"),
        html.P(description, style={"fontSize": "0.82rem", "color": "#475569", "marginBottom": "0.25rem"}),
        html.Span(source, style={"fontSize": "0.75rem", "color": "#94a3b8", "fontStyle": "italic"}),
    ], style={"background": "#f8fafc", "borderRadius": "0.5rem",
              "padding": "0.6rem 0.75rem", "borderLeft": f"3px solid {color}"})


def _score_card(label, score, color, is_composite=False, lang="cs"):
    bg = f"linear-gradient(135deg, {color}15 0%, white 100%)" if not is_composite else (
        "linear-gradient(135deg, #667eea20 0%, #764ba215 100%)"
    )
    return dbc.Card(
        dbc.CardBody(html.Div([
            html.Div(label, style={"fontSize": "0.78rem", "color": "#64748b",
                                   "fontWeight": "600", "marginBottom": "0.25rem"}),
            html.Div(f"{score:.1f}", style={
                "fontSize": "1.8rem" if is_composite else "1.5rem",
                "fontWeight": "800", "color": color, "lineHeight": "1.2"
            }),
            html.Div(t("score_per_100", lang), style={"fontSize": "0.72rem", "color": "#94a3b8"}),
        ])),
        className="shadow-sm text-center h-100",
        style={"border": f"1px solid {color}30", "borderRadius": "0.75rem", "background": bg}
    )


def layout(lang="cs"):
    all_scores = get_all_scores()
    domain_labels = [t(k, lang) for k in DOMAIN_LABEL_KEYS]

    district_options = sorted([{"label": d, "value": d} for d in all_scores.keys()],
                               key=lambda x: x["label"])
    default_district = "Praha 1"

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                page_title(
                    t("qol_title", lang),
                    align="center",
                    description=t("qol_desc", lang),
                    use_gradient=True
                ),

                dbc.Alert([
                    html.I(className="fa-solid fa-circle-info me-2"),
                    html.Strong(t("qol_methodology_prefix", lang)),
                    t("qol_methodology_note", lang),
                ], color="info", className="mb-4",
                   style={"fontSize": "0.88rem", "borderRadius": "0.75rem"}),

                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.I(className="fa-solid fa-chart-radar me-2",
                                   style={"color": "#667eea"}),
                            html.Span(t("qol_radar_title", lang),
                                      style={"fontWeight": "700", "fontSize": "1rem"}),
                        ], className="d-flex align-items-center")
                    ),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label(t("qol_select_district", lang),
                                           style={"fontWeight": "600", "fontSize": "0.9rem",
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
                        html.Div(id="qol-domain-cards"),
                    ])
                ], className="shadow-sm mb-4",
                   style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"}),

                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.I(className="fa-solid fa-ranking-star me-2",
                                   style={"color": "#f59e0b"}),
                            html.Span(t("qol_ranking_title", lang),
                                      style={"fontWeight": "700", "fontSize": "1rem"}),
                        ], className="d-flex align-items-center")
                    ),
                    dbc.CardBody([
                        dcc.Graph(
                            id="qol-ranking-chart",
                            figure=_create_ranking_chart(all_scores, lang),
                            config={"displayModeBar": False},
                            style={"height": f"{max(500, len(all_scores) * 26 + 80)}px",
                                   "cursor": "pointer"}
                        )
                    ])
                ], className="shadow-sm mb-4",
                   style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"}),

                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.I(className="fa-solid fa-list-check me-2",
                                   style={"color": "#0f766e"}),
                            html.Span(t("qol_domains_title", lang),
                                      style={"fontWeight": "700", "fontSize": "1rem"}),
                        ], className="d-flex align-items-center")
                    ),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(_domain_card(
                                "fa-shield-halved", t("qol_domain1_title", lang), "#0f766e",
                                t("qol_domain1_desc", lang), t("qol_domain1_source", lang)
                            ), md=6, className="mb-3"),
                            dbc.Col(_domain_card(
                                "fa-train-subway", t("qol_domain2_title", lang), "#1d4ed8",
                                t("qol_domain2_desc", lang), t("qol_domain2_source", lang)
                            ), md=6, className="mb-3"),
                            dbc.Col(_domain_card(
                                "fa-wheelchair", t("qol_domain3_title", lang), "#7c3aed",
                                t("qol_domain3_desc", lang), t("qol_domain3_source", lang)
                            ), md=6, className="mb-3"),
                            dbc.Col(_domain_card(
                                "fa-tree", t("qol_domain4_title", lang), "#16a34a",
                                t("qol_domain4_desc", lang), t("qol_domain4_source", lang)
                            ), md=6, className="mb-3"),
                        ])
                    ])
                ], className="shadow-sm",
                   style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"}),

            ], width=12)
        ])
    ], fluid=True, className="py-2")


@callback(
    Output("qol-radar-container", "children"),
    Output("qol-domain-cards", "children"),
    Input("qol-district-dropdown", "value"),
    Input("lang-store", "data"),
)
def update_radar(district, lang):
    lang = lang or "cs"
    scores = get_all_scores()
    if not district or district not in scores:
        return html.P(t("qol_select_prompt", lang)), None

    domain_scores = scores[district]
    composite = _composite_score(domain_scores)
    domain_labels = [t(k, lang) for k in DOMAIN_LABEL_KEYS]

    radar_fig = _create_radar_chart(district, domain_scores, lang)

    domain_cards = dbc.Row([
        dbc.Col(_score_card(domain_labels[i], domain_scores[i], DOMAIN_COLORS[i], lang=lang),
                xs=6, sm=3, className="mb-3")
        for i in range(4)
    ] + [
        dbc.Col(_score_card(t("score_composite", lang), composite, "#667eea",
                            is_composite=True, lang=lang),
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
