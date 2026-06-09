import dash_bootstrap_components as dbc
from dash import register_page, html
from src.components.ui import page_title
from src.i18n import t

register_page(__name__, path="/theory", name="Teorie")


def _section_card(icon_class, title, color, children):
    return dbc.Card([
        dbc.CardHeader(
            html.Div([
                html.I(className=f"fa-solid {icon_class}",
                       style={"fontSize": "1.3rem", "color": color, "marginRight": "0.6rem"}),
                html.Span(title, style={"fontWeight": "700", "fontSize": "1rem", "color": "#1e293b"}),
            ], className="d-flex align-items-center"),
            style={"background": "white", "border": "none", "paddingBottom": "0"}
        ),
        dbc.CardBody(children),
    ], className="shadow-sm mb-4", style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"})


def _domain_badge(label, color, text_color="white"):
    return html.Span(
        label,
        style={
            "display": "inline-block", "background": color, "color": text_color,
            "borderRadius": "12px", "padding": "4px 14px",
            "fontSize": "0.82rem", "fontWeight": "600",
            "marginRight": "0.4rem", "marginBottom": "0.4rem",
        }
    )


def _indicator_row(icon_class, label, description, color="#475569"):
    return html.Div([
        html.I(className=f"fa-solid {icon_class}",
               style={"fontSize": "1rem", "color": color, "minWidth": "1.5rem", "marginTop": "2px"}),
        html.Div([
            html.Span(label, style={"fontWeight": "600", "fontSize": "0.9rem", "color": "#1e293b"}),
            html.Span(f" — {description}", style={"fontSize": "0.88rem", "color": "#64748b"}),
        ], style={"marginLeft": "0.5rem"})
    ], className="d-flex align-items-start mb-2")


def _whoqol_domain_card(title, desc, bg, text_color):
    return html.Div([
        html.Span(title, style={"fontWeight": "700", "color": text_color}),
        html.P(desc, style={"fontSize": "0.82rem", "color": "#64748b", "margin": 0})
    ], style={"padding": "0.6rem", "background": bg, "borderRadius": "0.5rem", "marginBottom": "0.5rem"})


def layout(lang="cs"):
    # ── Obj vs Subj ─────────────────────────────────────────────────────────
    obj_vs_subj = _section_card(
        "fa-scale-balanced", t("theory_obj_subj_title", lang), "#667eea",
        [
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(className="fa-solid fa-ruler-combined",
                               style={"fontSize": "2rem", "color": "#3b82f6", "marginBottom": "0.5rem"}),
                        html.H6(t("theory_obj_title", lang), style={"fontWeight": "700", "color": "#1e293b"}),
                        html.P(t("theory_obj_desc", lang),
                               style={"fontSize": "0.88rem", "color": "#475569", "lineHeight": "1.5"}),
                        html.Div([
                            _domain_badge(t("theory_obj_badge_metro", lang), "#dbeafe", "#1e3a8a"),
                            _domain_badge(t("theory_obj_badge_ztp", lang), "#ede9fe", "#4c1d95"),
                            _domain_badge(t("theory_obj_badge_police", lang), "#dcfce7", "#14532d"),
                        ])
                    ], style={"padding": "1rem", "background": "#f8faff",
                              "borderRadius": "0.75rem", "height": "100%"})
                ], md=6, className="mb-3"),
                dbc.Col([
                    html.Div([
                        html.I(className="fa-solid fa-heart-pulse",
                               style={"fontSize": "2rem", "color": "#a855f7", "marginBottom": "0.5rem"}),
                        html.H6(t("theory_subj_title", lang), style={"fontWeight": "700", "color": "#1e293b"}),
                        html.P(t("theory_subj_desc", lang),
                               style={"fontSize": "0.88rem", "color": "#475569", "lineHeight": "1.5"}),
                        html.Div([
                            _domain_badge(t("theory_subj_badge_housing", lang), "#fae8ff", "#701a75"),
                            _domain_badge(t("theory_subj_badge_safety", lang), "#fef3c7", "#78350f"),
                            _domain_badge(t("theory_subj_badge_swb", lang), "#ffe4e6", "#881337"),
                        ])
                    ], style={"padding": "1rem", "background": "#fdf8ff",
                              "borderRadius": "0.75rem", "height": "100%"})
                ], md=6, className="mb-3"),
            ]),
            html.Div(
                html.P([
                    html.I(className="fa-solid fa-quote-left",
                           style={"color": "#94a3b8", "marginRight": "0.5rem"}),
                    t("theory_ssf_quote", lang),
                    html.Span(" — Stiglitz-Sen-Fitoussi Commission (2009)",
                              style={"color": "#94a3b8"})
                ], style={"fontSize": "0.88rem", "color": "#475569", "marginBottom": 0}),
                style={"background": "#f8fafc", "borderLeft": "4px solid #667eea",
                       "padding": "0.75rem 1rem", "borderRadius": "0 0.5rem 0.5rem 0"}
            )
        ]
    )

    # ── QOUL 4 domains ──────────────────────────────────────────────────────
    qoul_domains = _section_card(
        "fa-city", t("theory_qoul_title", lang), "#0f766e",
        [
            html.P(t("theory_qoul_desc", lang),
                   style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1rem"}),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Span("1", style={"background": "#0f766e", "color": "white",
                                                  "borderRadius": "50%", "padding": "2px 8px",
                                                  "fontWeight": "700", "marginRight": "0.5rem"}),
                            html.Span(t("theory_domain1_name", lang),
                                      style={"fontWeight": "700", "color": "#134e4a"}),
                        ], className="d-flex align-items-center mb-2"),
                        _indicator_row("fa-shield-halved", t("theory_domain1_i1", lang),
                                       t("theory_domain1_i1d", lang), "#0f766e"),
                        _indicator_row("fa-building-shield", t("theory_domain1_i2", lang),
                                       t("theory_domain1_i2d", lang), "#0f766e"),
                    ], style={"padding": "0.85rem", "background": "#f0fdfa",
                              "borderRadius": "0.75rem", "height": "100%"})
                ], md=6, className="mb-3"),
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Span("2", style={"background": "#1d4ed8", "color": "white",
                                                  "borderRadius": "50%", "padding": "2px 8px",
                                                  "fontWeight": "700", "marginRight": "0.5rem"}),
                            html.Span(t("theory_domain2_name", lang),
                                      style={"fontWeight": "700", "color": "#1e3a8a"}),
                        ], className="d-flex align-items-center mb-2"),
                        _indicator_row("fa-train-subway", t("theory_domain2_i1", lang),
                                       t("theory_domain2_i1d", lang), "#1d4ed8"),
                        _indicator_row("fa-elevator", t("theory_domain2_i2", lang),
                                       t("theory_domain2_i2d", lang), "#1d4ed8"),
                        _indicator_row("fa-car-side", t("theory_domain2_i3", lang),
                                       t("theory_domain2_i3d", lang), "#1d4ed8"),
                    ], style={"padding": "0.85rem", "background": "#eff6ff",
                              "borderRadius": "0.75rem", "height": "100%"})
                ], md=6, className="mb-3"),
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Span("3", style={"background": "#7c3aed", "color": "white",
                                                  "borderRadius": "50%", "padding": "2px 8px",
                                                  "fontWeight": "700", "marginRight": "0.5rem"}),
                            html.Span(t("theory_domain3_name", lang),
                                      style={"fontWeight": "700", "color": "#4c1d95"}),
                        ], className="d-flex align-items-center mb-2"),
                        _indicator_row("fa-wheelchair", t("theory_domain3_i1", lang),
                                       t("theory_domain3_i1d", lang), "#7c3aed"),
                        _indicator_row("fa-stairs", t("theory_domain3_i2", lang),
                                       t("theory_domain3_i2d", lang), "#7c3aed"),
                        _indicator_row("fa-map-pin", t("theory_domain3_i3", lang),
                                       t("theory_domain3_i3d", lang), "#7c3aed"),
                    ], style={"padding": "0.85rem", "background": "#faf5ff",
                              "borderRadius": "0.75rem", "height": "100%"})
                ], md=6, className="mb-3"),
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Span("4", style={"background": "#b45309", "color": "white",
                                                  "borderRadius": "50%", "padding": "2px 8px",
                                                  "fontWeight": "700", "marginRight": "0.5rem"}),
                            html.Span(t("theory_domain4_name", lang),
                                      style={"fontWeight": "700", "color": "#78350f"}),
                        ], className="d-flex align-items-center mb-2"),
                        _indicator_row("fa-wind", t("theory_domain4_i1", lang),
                                       t("theory_domain4_i1d", lang), "#b45309"),
                        _indicator_row("fa-tree", t("theory_domain4_i2", lang),
                                       t("theory_domain4_i2d", lang), "#b45309"),
                        _indicator_row("fa-volume-high", t("theory_domain4_i3", lang),
                                       t("theory_domain4_i3d", lang), "#b45309"),
                    ], style={"padding": "0.85rem", "background": "#fffbeb",
                              "borderRadius": "0.75rem", "height": "100%"})
                ], md=6, className="mb-3"),
            ])
        ]
    )

    # ── 15-Minute City ───────────────────────────────────────────────────────
    fifteen_min = _section_card(
        "fa-person-walking", t("theory_15min_title", lang), "#dc2626",
        [
            html.P(t("theory_15min_desc", lang),
                   style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1rem"}),
            dbc.Row([
                dbc.Col([
                    html.H6(t("theory_15min_functions_title", lang),
                            style={"fontWeight": "700", "color": "#7f1d1d", "marginBottom": "0.5rem"}),
                    html.Div([
                        _domain_badge(t("theory_15min_fn_housing", lang), "#fee2e2", "#7f1d1d"),
                        _domain_badge(t("theory_15min_fn_work", lang), "#fef3c7", "#78350f"),
                        _domain_badge(t("theory_15min_fn_shopping", lang), "#dcfce7", "#14532d"),
                        _domain_badge(t("theory_15min_fn_health", lang), "#dbeafe", "#1e3a8a"),
                        _domain_badge(t("theory_15min_fn_education", lang), "#ede9fe", "#4c1d95"),
                        _domain_badge(t("theory_15min_fn_leisure", lang), "#fce7f3", "#831843"),
                    ], style={"marginBottom": "1rem"})
                ], md=6),
                dbc.Col([
                    html.H6(t("theory_15min_dimensions_title", lang),
                            style={"fontWeight": "700", "color": "#7f1d1d", "marginBottom": "0.5rem"}),
                    _indicator_row("fa-users", t("theory_15min_d_density", lang),
                                   t("theory_15min_d_density_desc", lang), "#dc2626"),
                    _indicator_row("fa-location-dot", t("theory_15min_d_proximity", lang),
                                   t("theory_15min_d_proximity_desc", lang), "#dc2626"),
                    _indicator_row("fa-shuffle", t("theory_15min_d_diversity", lang),
                                   t("theory_15min_d_diversity_desc", lang), "#dc2626"),
                    _indicator_row("fa-wifi", t("theory_15min_d_digital", lang),
                                   t("theory_15min_d_digital_desc", lang), "#dc2626"),
                ], md=6),
            ]),
            html.Div(
                html.P([
                    html.I(className="fa-solid fa-triangle-exclamation",
                           style={"color": "#f59e0b", "marginRight": "0.5rem"}),
                    html.Strong("Important: " if lang == "en" else "Důležité: "),
                    t("theory_15min_note", lang),
                ], style={"fontSize": "0.88rem", "color": "#475569", "marginBottom": 0}),
                style={"background": "#fffbeb", "borderLeft": "4px solid #f59e0b",
                       "padding": "0.75rem 1rem", "borderRadius": "0 0.5rem 0.5rem 0"}
            )
        ]
    )

    # ── WHOQOL ───────────────────────────────────────────────────────────────
    whoqol = _section_card(
        "fa-hospital", t("theory_whoqol_title", lang), "#0369a1",
        [
            html.P(t("theory_whoqol_desc", lang),
                   style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1rem"}),
            dbc.Row([
                dbc.Col([
                    _whoqol_domain_card(t("theory_whoqol_d1", lang), t("theory_whoqol_d1_sub", lang),
                                        "#f0f9ff", "#0369a1"),
                    _whoqol_domain_card(t("theory_whoqol_d2", lang), t("theory_whoqol_d2_sub", lang),
                                        "#faf5ff", "#7c3aed"),
                    _whoqol_domain_card(t("theory_whoqol_d3", lang), t("theory_whoqol_d3_sub", lang),
                                        "#f0fdfa", "#0f766e"),
                ], md=6),
                dbc.Col([
                    _whoqol_domain_card(t("theory_whoqol_d4", lang), t("theory_whoqol_d4_sub", lang),
                                        "#fdf2f8", "#be185d"),
                    _whoqol_domain_card(t("theory_whoqol_d5", lang), t("theory_whoqol_d5_sub", lang),
                                        "#fffbeb", "#b45309"),
                    _whoqol_domain_card(t("theory_whoqol_d6", lang), t("theory_whoqol_d6_sub", lang),
                                        "#f9fafb", "#6b7280"),
                ], md=6),
            ])
        ]
    )

    # ── Personas ─────────────────────────────────────────────────────────────
    def _persona_mini_card(icon, name, loc, items, bg, border, color):
        return dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.I(className=f"fa-solid {icon}",
                           style={"fontSize": "1.8rem", "color": color}),
                    html.Div([
                        html.Div(name, style={"fontWeight": "700", "color": color}),
                        html.Div(loc, style={"fontSize": "0.8rem", "color": "#64748b"}),
                    ], style={"marginLeft": "0.5rem"})
                ], className="d-flex align-items-center mb-2"),
                html.Ul([html.Li(item, style={"fontSize": "0.82rem"}) for item in items],
                        style={"paddingLeft": "1rem", "marginBottom": 0})
            ])
        ], style={"borderRadius": "0.75rem", "border": f"1px solid {border}", "background": bg})

    personas_section = _section_card(
        "fa-people-group", t("theory_personas_title", lang), "#7c3aed",
        [
            html.P(t("theory_personas_desc", lang),
                   style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1rem"}),
            dbc.Row([
                dbc.Col(_persona_mini_card(
                    "fa-person-cane", t("theory_jan_name", lang), t("theory_jan_loc", lang),
                    [t("theory_jan_li1", lang), t("theory_jan_li2", lang),
                     t("theory_jan_li3", lang), t("theory_jan_li4", lang)],
                    "#f0fdfa", "#d1fae5", "#0f766e"
                ), md=4, className="mb-3"),
                dbc.Col(_persona_mini_card(
                    "fa-person-biking", t("theory_elena_name", lang), t("theory_elena_loc", lang),
                    [t("theory_elena_li1", lang), t("theory_elena_li2", lang),
                     t("theory_elena_li3", lang), t("theory_elena_li4", lang)],
                    "#eff6ff", "#dbeafe", "#1d4ed8"
                ), md=4, className="mb-3"),
                dbc.Col(_persona_mini_card(
                    "fa-people-roof", t("theory_novak_name", lang), t("theory_novak_loc", lang),
                    [t("theory_novak_li1", lang), t("theory_novak_li2", lang),
                     t("theory_novak_li3", lang), t("theory_novak_li4", lang)],
                    "#fffbeb", "#fde68a", "#b45309"
                ), md=4, className="mb-3"),
            ]),
        ]
    )

    # ── Measurement ──────────────────────────────────────────────────────────
    measurement = _section_card(
        "fa-chart-line", t("theory_measurement_title", lang), "#6b7280",
        [
            dbc.Row([
                dbc.Col([
                    html.H6(t("theory_oecd_title", lang),
                            style={"fontWeight": "700", "color": "#1e293b", "fontSize": "0.9rem"}),
                    html.P(t("theory_oecd_desc", lang),
                           style={"fontSize": "0.82rem", "color": "#475569"}),
                ], md=4),
                dbc.Col([
                    html.H6(t("theory_wbcsd_title", lang),
                            style={"fontWeight": "700", "color": "#1e293b", "fontSize": "0.9rem"}),
                    html.P(t("theory_wbcsd_desc", lang),
                           style={"fontSize": "0.82rem", "color": "#475569"}),
                ], md=4),
                dbc.Col([
                    html.H6(t("theory_diener_title", lang),
                            style={"fontWeight": "700", "color": "#1e293b", "fontSize": "0.9rem"}),
                    html.P(t("theory_diener_desc", lang),
                           style={"fontSize": "0.82rem", "color": "#475569"}),
                ], md=4),
            ])
        ]
    )

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                page_title(
                    t("theory_title", lang),
                    align="center",
                    description=t("theory_desc", lang),
                    use_gradient=True
                ),
                obj_vs_subj,
                qoul_domains,
                fifteen_min,
                whoqol,
                personas_section,
                measurement,
            ], width=12)
        ])
    ], fluid=True, className="py-2")
