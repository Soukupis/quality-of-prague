import dash_bootstrap_components as dbc
from dash import html

from ..ui import icon, nav_item
from ..config import SIDEBAR_STYLE, NAV_ITEMS, TEXT_COLOR, FONT_WEIGHT_BOLD, FONT_SIZE_LARGE, SPACING_XL

def sidebar_header():
    return html.Div([
        html.H3([
            icon(name="list", class_name="me-2"),
            "Navigace"
        ], className="mb-0", style={
            "color": TEXT_COLOR,
            "fontWeight": FONT_WEIGHT_BOLD,
            "fontSize": FONT_SIZE_LARGE
        }),
    ], style={"padding": f"0 {SPACING_XL}", "marginBottom": SPACING_XL})

def _render_nav_item(item):
    if item.get("type") == "divider":
        return html.Div(
            item["label"],
            style={
                "fontSize": "0.7rem",
                "color": "#94a3b8",
                "fontWeight": "700",
                "letterSpacing": "0.08em",
                "textTransform": "uppercase",
                "padding": "0.75rem 1.5rem 0.25rem",
            }
        )
    return nav_item(
        label=item["label"],
        href=item["href"],
        icon_name=item["icon"],
        variant="sidebar"
    )


def sidebar():
    return html.Div([
    sidebar_header(),
    dbc.Nav(
        [_render_nav_item(item) for item in NAV_ITEMS],
        vertical=True,
        className="flex-column",
        style={"padding": "0 1rem"}
    ),
], style=SIDEBAR_STYLE)