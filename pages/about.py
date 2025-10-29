import dash_bootstrap_components as dbc
from dash import register_page
from components.ui.page_heading import page_title, page_subtitle, page_divider

register_page(__name__, path="/about", name="About")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            page_title("About", icon_name="info-circle"),
            page_subtitle("Quality of Prague is a platform for analyzing and presenting quality of life metrics for Prague."),
            page_divider()
        ], width=12)
    ]),
], fluid=True, className="py-1")
