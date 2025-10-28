import dash_bootstrap_components as dbc

from ..ui import brand, nav_item
from ..config import NAVBAR_STYLE, NAV_ITEMS, BRAND_CONFIG

navbar = dbc.Navbar(
    dbc.Container([
        brand(**BRAND_CONFIG),
    ], fluid=True, className="px-4"),
    color="light",
    fixed="top",
    className="shadow-sm border-0",
    style=NAVBAR_STYLE,
)
