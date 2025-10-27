import dash_bootstrap_components as dbc
from dash import html, register_page

register_page(__name__, path="/about", name="About")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("About Quality of Prague", className="display-4 mb-4"),
            html.P(
                "Quality of Prague is a comprehensive platform dedicated to analyzing "
                "and presenting quality of life metrics for the beautiful city of Prague.",
                className="lead mb-4"
            ),
            html.Hr(className="mb-4")
        ], width=12)
    ], className="text-center mb-5"),
], fluid=True, className="py-1")
