import dash_bootstrap_components as dbc
from dash import register_page
from src.components.ui import page_title, page_subtitle, page_divider

register_page(__name__, path="/dashboard", name="Dashboard")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            page_title("Dashboard", icon_name="bar-chart"),
            page_subtitle("Poznatky a metriky týkající se ukazatelů kvality života v Praze."),
            page_divider()
        ], width=12)
    ]),
], fluid=True, className="py-2")
