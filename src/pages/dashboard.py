import dash_bootstrap_components as dbc
from dash import register_page
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
], fluid=True, className="py-2")
