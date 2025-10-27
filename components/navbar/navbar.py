import dash_bootstrap_components as dbc
from dash import html

from ..ui import brand, nav_item
from ..config import NAVBAR_STYLE, NAV_ITEMS, BRAND_CONFIG

navbar = dbc.Navbar(
    dbc.Container([
        brand(**BRAND_CONFIG),
        dbc.Nav([
            nav_item(
                label=item["label"],
                href=item["href"],
                icon_name=item["icon"],
                variant="navbar"
            ) for item in NAV_ITEMS if item["label"] in ["Dashboard", "Districts", "About"]
        ], className="ms-auto", navbar=True),
    ], fluid=True, className="px-4"),
    color="light",
    fixed="top",
    className="shadow-sm border-0",
    style=NAVBAR_STYLE,
)