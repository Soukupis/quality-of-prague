import dash_bootstrap_components as dbc
from dash import register_page
from src.components.ui import page_title

register_page(__name__, path="/about", name="O Aplikaci")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            page_title(
                "O Aplikaci",
                align="center",
                description="Quality of Prague je platforma pro analýzu a prezentaci ukazatelů kvality života v Praze.",
                use_gradient=True
            )
        ], width=12)
    ]),
], fluid=True, className="py-1")
