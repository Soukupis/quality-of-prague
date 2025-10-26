import dash_bootstrap_components as dbc
from dash import html

from ..ui import icon, nav_item
from ..config import SIDEBAR_STYLE, NAV_ITEMS, TEXT_COLOR, FONT_WEIGHT_BOLD, FONT_SIZE_LARGE, SPACING_XL

def sidebar_header():
    return html.Div([
        html.H3([
            icon(name="list", class_name="me-2"),
            "Navigation"
        ], className="mb-0", style={
            "color": TEXT_COLOR,
            "fontWeight": FONT_WEIGHT_BOLD,
            "fontSize": FONT_SIZE_LARGE
        }),
    ], style={"padding": f"0 {SPACING_XL}", "marginBottom": SPACING_XL})

sidebar = html.Div([
    sidebar_header(),
    dbc.Nav([
        nav_item(
            label=item["label"],
            href=item["href"],
            icon_name=item["icon"],
            variant="sidebar"
        ) for item in NAV_ITEMS
    ],
    vertical=True,
    className="flex-column",
    style={"padding": "0 1rem"}),
], style=SIDEBAR_STYLE)

__all__ = ["sidebar"]
