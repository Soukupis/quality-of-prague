import dash_bootstrap_components as dbc
from dash import register_page, dcc, html
from src.components.pages.dashboard import district_select, data_select
from src.components.ui import page_title

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
            dbc.Card(
                dcc.Loading(
                    id="loading-chart",
                    type="circle",
                    children=html.Div(id="chart_container"),
                    color="#3b82f6",
                    fullscreen=False,
                    style={"minHeight": "400px"},
                    overlay_style={"visibility": "visible", "opacity": 0.5}
                )
            )
        ]),
        dbc.Col([
        ])
    ])
], fluid=True, className="py-2")
