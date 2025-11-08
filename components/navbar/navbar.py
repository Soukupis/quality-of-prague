import dash_bootstrap_components as dbc

from components.ui import brand
from components.config import NAVBAR_STYLE, BRAND_CONFIG

def navbar():
    return dbc.Navbar(
    dbc.Container([
        brand(**BRAND_CONFIG),
    ], fluid=True, className="px-4"),
    color="light",
    fixed="top",
    className="shadow-sm border-0",
    style=NAVBAR_STYLE,
)
