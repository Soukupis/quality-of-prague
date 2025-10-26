#TODO: Dashboard Layout
import dash_bootstrap_components as dbc
from dash import html, register_page

register_page(__name__, path="/dashboard", name="Dashboard")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Prague Quality Dashboard", className="display-4 mb-2"),
            html.P(
                "Real-time insights and metrics about Prague's quality of life indicators.",
                className="lead mb-4"
            ),
            html.Hr(className="mb-4")
        ], width=12)
    ]),
], fluid=True, className="py-4")
