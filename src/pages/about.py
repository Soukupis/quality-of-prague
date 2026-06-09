"""About page for the Quality of Prague application."""
import dash_bootstrap_components as dbc
from dash import register_page, html
from src.components.ui import page_title
from src.i18n import t

register_page(__name__, path="/about", name="O Aplikaci")


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


def _framework_mini_card(title, subtitle, items, bg, border, title_color):
    return dbc.Card([
        dbc.CardBody([
            html.Div(title, style={"fontWeight": "700", "fontSize": "0.9rem",
                                   "color": title_color, "marginBottom": "0.2rem"}),
            html.Div(subtitle, style={"fontSize": "0.78rem", "color": "#64748b",
                                      "marginBottom": "0.5rem"}),
            html.Ul([
                html.Li(item, style={"fontSize": "0.8rem", "color": "#475569"})
                for item in items
            ], style={"paddingLeft": "1.1rem", "marginBottom": 0})
        ], style={"padding": "0.75rem 1rem"})
    ], style={"background": bg, "border": f"1px solid {border}",
              "borderRadius": "0.75rem", "height": "100%"})


def _dataset_chip(label):
    return html.Span(
        label,
        style={
            "display": "inline-block", "background": "#f0fdf4", "color": "#166534",
            "borderRadius": "1rem", "padding": "2px 10px",
            "fontSize": "0.82rem", "fontWeight": "600",
            "marginRight": "0.4rem", "marginBottom": "0.5rem",
        }
    )


def _nav_row(icon_class, page_name, description, color):
    return html.Div([
        html.I(className=f"fa-solid {icon_class}",
               style={"fontSize": "1rem", "color": color,
                      "minWidth": "1.5rem", "marginTop": "2px"}),
        html.Div([
            html.Span(page_name, style={"fontWeight": "700", "fontSize": "0.9rem", "color": "#1e293b"}),
            html.Span(f" — {description}", style={"fontSize": "0.88rem", "color": "#64748b"}),
        ], style={"marginLeft": "0.6rem"})
    ], className="d-flex align-items-start mb-3")


def layout(lang="cs"):
    DATASETS = [
        "Hranice městských částí (IPR Praha)",
        "Objekty Městské policie (Geoportál Praha)",
        "Parkovací automaty (Geoportál Praha)",
        "Stání ZTP (Geoportál Praha)",
        "P+R parkoviště (Geoportál Praha)",
        "Placené stání (Geoportál Praha)",
        "Zákazy stání (Geoportál Praha)",
        "Vstupy do metra (Geoportál Praha)",
        "Parky a zeleň (OpenStreetMap / Overpass API)",
        "Nextbike stanice (GBFS v2.3)",
        "Zastávky PID (Ropid open data)",
        "Stanice kvality ovzduší (ČHMÚ)",
        "Demografické údaje MČ (ČSÚ, 2004–2025)",
    ]

    intro = _section_card(
        "fa-city", t("about_intro_title", lang), "#667eea",
        [
            html.P(t("about_intro_desc", lang),
                   style={"fontSize": "0.9rem", "color": "#475569", "lineHeight": "1.6",
                           "marginBottom": "1rem"}),
            html.Div([
                html.Div([
                    html.I(className="fa-solid fa-graduation-cap",
                           style={"fontSize": "1.1rem", "color": "#667eea", "marginRight": "0.5rem"}),
                    html.Span(t("about_origin_title", lang),
                              style={"fontWeight": "700", "color": "#1e293b"}),
                ], className="d-flex align-items-center mb-2"),
                html.P([
                    t("about_origin_desc", lang) + " ",
                    html.Em(t("about_thesis_title", lang), style={"color": "#4f46e5"}),
                    " " + t("about_thesis_author", lang),
                ], style={"fontSize": "0.88rem", "color": "#475569", "marginBottom": 0}),
            ], style={"background": "#f5f3ff", "borderLeft": "4px solid #667eea",
                      "padding": "0.85rem 1rem", "borderRadius": "0 0.75rem 0.75rem 0",
                      "marginBottom": "1rem"}),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(className="fa-solid fa-bullseye",
                               style={"fontSize": "1.5rem", "color": "#667eea", "marginBottom": "0.4rem"}),
                        html.H6(t("about_goal_title", lang), style={"fontWeight": "700", "color": "#1e293b"}),
                        html.P(t("about_goal_desc", lang),
                               style={"fontSize": "0.83rem", "color": "#475569", "marginBottom": 0}),
                    ], style={"padding": "0.85rem", "background": "#fafafa",
                              "borderRadius": "0.75rem", "height": "100%",
                              "border": "1px solid #e2e8f0"})
                ], md=4, className="mb-3"),
                dbc.Col([
                    html.Div([
                        html.I(className="fa-solid fa-map-location-dot",
                               style={"fontSize": "1.5rem", "color": "#0ea5e9", "marginBottom": "0.4rem"}),
                        html.H6(t("about_scope_title", lang), style={"fontWeight": "700", "color": "#1e293b"}),
                        html.P(t("about_scope_desc", lang),
                               style={"fontSize": "0.83rem", "color": "#475569", "marginBottom": 0}),
                    ], style={"padding": "0.85rem", "background": "#f0f9ff",
                              "borderRadius": "0.75rem", "height": "100%",
                              "border": "1px solid #bae6fd"})
                ], md=4, className="mb-3"),
                dbc.Col([
                    html.Div([
                        html.I(className="fa-solid fa-database",
                               style={"fontSize": "1.5rem", "color": "#10b981", "marginBottom": "0.4rem"}),
                        html.H6(t("about_data_title", lang), style={"fontWeight": "700", "color": "#1e293b"}),
                        html.P(t("about_data_desc", lang),
                               style={"fontSize": "0.83rem", "color": "#475569", "marginBottom": 0}),
                    ], style={"padding": "0.85rem", "background": "#f0fdf4",
                              "borderRadius": "0.75rem", "height": "100%",
                              "border": "1px solid #bbf7d0"})
                ], md=4, className="mb-3"),
            ])
        ]
    )

    theory_section = _section_card(
        "fa-book-open", t("about_theory_title", lang), "#764ba2",
        [
            html.P(t("about_theory_desc", lang),
                   style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1rem",
                           "lineHeight": "1.6"}),
            dbc.Row([
                dbc.Col([
                    _framework_mini_card(
                        "WHOQOL (WHO)",
                        "6 domains of individual well-being" if lang == "en" else "6 domén individuální pohody",
                        [
                            t("theory_whoqol_d1", lang) + " — " + t("theory_whoqol_d1_sub", lang),
                            t("theory_whoqol_d2", lang) + " — " + t("theory_whoqol_d2_sub", lang),
                            t("theory_whoqol_d3", lang) + " — " + t("theory_whoqol_d3_sub", lang),
                            t("theory_whoqol_d4", lang) + " — " + t("theory_whoqol_d4_sub", lang),
                            t("theory_whoqol_d5", lang) + " — " + t("theory_whoqol_d5_sub", lang),
                            t("theory_whoqol_d6", lang),
                        ],
                        "#f0f9ff", "#bae6fd", "#0369a1"
                    )
                ], md=6, className="mb-3"),
                dbc.Col([
                    _framework_mini_card(
                        "QOUL — " + (
                            "4 operational domains" if lang == "en" else "4 operační domény"
                        ),
                        "Základ analytické struktury dashboardu" if lang == "cs"
                        else "Basis of the dashboard's analytical structure",
                        [
                            t("theory_domain1_name", lang),
                            t("theory_domain2_name", lang) + " — MHD, intermodality" if lang == "en"
                            else t("theory_domain2_name", lang) + " — MHD, intermodalita",
                            t("theory_domain3_name", lang),
                            t("theory_domain4_name", lang),
                        ],
                        "#f0fdfa", "#99f6e4", "#0f766e"
                    )
                ], md=6, className="mb-3"),
                dbc.Col([
                    _framework_mini_card(
                        "15-Minute City (Moreno et al., 2021)",
                        "6 " + ("functions, 4 dimensions" if lang == "en" else "funkcí, 4 dimenze realizace"),
                        [
                            (
                                "Functions: housing, work, shopping, health, education, leisure"
                                if lang == "en" else
                                "Funkce: bydlení, práce, nákupy, zdraví, vzdělání, volný čas"
                            ),
                            t("theory_15min_d_density", lang) + " — " + t("theory_15min_d_density_desc", lang),
                            t("theory_15min_d_proximity", lang) + " — " + t("theory_15min_d_proximity_desc", lang),
                            t("theory_15min_d_diversity", lang) + " — " + t("theory_15min_d_diversity_desc", lang),
                            t("theory_15min_d_digital", lang) + " — " + t("theory_15min_d_digital_desc", lang),
                        ],
                        "#fff1f2", "#fecdd3", "#be123c"
                    )
                ], md=6, className="mb-3"),
                dbc.Col([
                    _framework_mini_card(
                        "Stiglitz-Sen-Fitoussi Commission",
                        (
                            "Objective indicators vs. subjective well-being"
                            if lang == "en" else
                            "Objektivní ukazatele vs. subjektivní pohoda"
                        ),
                        [
                            (
                                "Separating objective measurements from subjective experience"
                                if lang == "en" else
                                "Oddělení objektivních měření od subjektivního prožitku"
                            ),
                            (
                                "Commission recommendations for national statistics (2009)"
                                if lang == "en" else
                                "Doporučení pro národní statistiky (2009)"
                            ),
                            "\"" + t("theory_ssf_quote", lang)[:60] + "...\"",
                            (
                                "Basis for the two-layer approach in this dashboard"
                                if lang == "en" else
                                "Základ pro dvouvrstvý přístup v tomto dashboardu"
                            ),
                        ],
                        "#faf5ff", "#e9d5ff", "#7c3aed"
                    )
                ], md=6, className="mb-3"),
            ])
        ]
    )

    datasets_section = _section_card(
        "fa-database", t("about_datasets_title", lang), "#0f766e",
        [
            html.P(t("about_datasets_desc", lang),
                   style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1rem",
                           "lineHeight": "1.6"}),
            html.Div(
                [_dataset_chip(ds) for ds in DATASETS],
                style={"display": "flex", "flexWrap": "wrap", "gap": "0"}
            ),
            html.Div([
                html.I(className="fa-solid fa-circle-info",
                       style={"color": "#0f766e", "marginRight": "0.5rem", "fontSize": "0.9rem"}),
                html.Span(t("about_datasets_note", lang),
                          style={"fontSize": "0.85rem", "color": "#475569"})
            ], className="d-flex align-items-start mt-3",
               style={"background": "#f0fdf4", "padding": "0.75rem 1rem",
                      "borderRadius": "0.75rem", "border": "1px solid #bbf7d0"})
        ]
    )

    navigation_section = _section_card(
        "fa-compass", t("about_nav_title", lang), "#d97706",
        [
            html.P(t("about_nav_desc", lang),
                   style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1.25rem",
                           "lineHeight": "1.6"}),
            _nav_row("fa-house",        t("nav_home", lang),       t("about_nav_home_desc", lang),     "#667eea"),
            _nav_row("fa-location-dot", t("nav_districts", lang),  t("about_nav_districts_desc", lang),"#0ea5e9"),
            _nav_row("fa-map-pin",
                     t("district_detail_name", lang),              t("about_nav_detail_desc", lang),   "#10b981"),
            _nav_row("fa-chart-bar",    t("nav_dashboard", lang),  t("about_nav_dashboard_desc", lang),"#f59e0b"),
            _nav_row("fa-chart-line",   t("nav_qol_index", lang),  t("about_nav_qol_desc", lang),      "#8b5cf6"),
            _nav_row("fa-book",         t("nav_theory", lang),     t("about_nav_theory_desc", lang),   "#764ba2"),
            _nav_row("fa-people-group", t("nav_personas", lang),   t("about_nav_personas_desc", lang), "#be185d"),
            _nav_row("fa-database",     t("nav_datasets", lang),   t("about_nav_datasets_desc", lang), "#0f766e"),
        ]
    )

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                page_title(t("about_title", lang), align="center", use_gradient=True),
                intro,
                theory_section,
                datasets_section,
                navigation_section,
            ], width=12)
        ])
    ], fluid=True, className="py-2")
