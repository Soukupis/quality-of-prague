import dash_bootstrap_components as dbc
from dash import register_page
from src.components.ui import page_title, page_subtitle, page_divider

register_page(__name__, path="/about", name="O Aplikaci")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            page_title("O Aplikaci", icon_name="info-circle"),
            page_subtitle("Quality of Prague je platforma pro analýzu a prezentaci ukazatelů kvality života v Praze."),
            page_divider()
        ], width=12)
    ]),
], fluid=True, className="py-1")
