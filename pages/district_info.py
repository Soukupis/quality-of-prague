import dash_bootstrap_components as dbc
from dash import html, register_page, dcc

register_page(__name__, path="/district-detail", name="Districts Detail")

def layout(district=None, **kwargs):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1(district, className="text-center")
            ], width=12)
        ])
    ], fluid=True, className="py-1")

