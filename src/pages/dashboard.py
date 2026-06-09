"""Dashboard page for comparing quality of life metrics across districts.

This page provides an interactive dashboard where users can select multiple
Prague districts and a dataset to compare metrics in a bar chart visualization.
Includes district and dataset selection dropdowns with a comparison chart.
"""
import dash_bootstrap_components as dbc
from dash import register_page, dcc, html
from src.components.pages.dashboard import district_select, data_select
from src.components.ui import page_title

NORMALIZATION_OPTIONS = [
    {"label": "Počet objektů", "value": "count"},
    {"label": "Hustota (/ km²)", "value": "density"},
]

register_page(__name__, path="/dashboard", name="Dashboard")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            page_title(
                "Dashboard",
                align="center",
                description="Poznatky a metriky týkající se ukazatelů kvality života v Praze.",
                use_gradient=True
            )
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            district_select()
        ], width=6, className="mb-4"),
        dbc.Col([
            data_select()
        ], width=6, className="mb-4"),
    ], className="mt-4"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="bi bi-calculator",
                               style={"fontSize": "1.1rem", "color": "#667eea", "marginRight": "0.5rem"}),
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
                ])
            ], className="shadow-sm", style={
                "border": "none",
                "borderRadius": "1rem",
                "background": "linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%)"
            })
        ], width=12, className="mb-3")
    ], className="mt-2"),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dcc.Loading(
                    id="loading_bar_chart",
                    type="circle",
                    children=html.Div(id="bar_chart_container"),
                    color="#3b82f6",
                    fullscreen=False,
                    style={"minHeight": "400px"},
                    overlay_style={"visibility": "visible", "opacity": 0.5}
                )
            )
        ]),
        dbc.Col([
            dbc.Card(
                dcc.Loading(
                    id="loading_district_map",
                    type="circle",
                    children=html.Div(id="district_map_container"),
                    color="#3b82f6",
                    fullscreen=False,
                    style={"minHeight": "400px"},
                    overlay_style={"visibility": "visible", "opacity": 0.5}
                )
            )
        ]),
    ])
], fluid=True, className="py-2")
