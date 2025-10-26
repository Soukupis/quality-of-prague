import dash_bootstrap_components as dbc
from dash import html
from typing import Union, Literal
from .icon import icon
from ..config import PRIMARY_COLOR, ICON_SIZE_SMALL, ICON_SIZE_MEDIUM, FONT_WEIGHT_MEDIUM, SPACING_MEDIUM


def nav_item(
    label: str,
    href: str,
    icon_name: str,
    variant: str = "navbar",
    active: Union[Literal["partial", "exact"], bool, None] = "exact",
    icon_size: str = ICON_SIZE_SMALL,
    icon_color: str = PRIMARY_COLOR
) -> Union[dbc.NavItem, dbc.NavLink]:
    if variant == "navbar":
        return dbc.NavItem(
            dbc.NavLink([
                icon(name=icon_name, size=icon_size, color=icon_color, class_name="me-1"),
                label
            ], href=href, className="nav-link-modern px-2")
        )

    elif variant == "sidebar":
        return dbc.NavLink([
            html.Div([
                icon(
                    name=icon_name,
                    size=ICON_SIZE_MEDIUM,
                    color=icon_color,
                    style={"marginRight": SPACING_MEDIUM}
                ),
                html.Span(label, style={"fontWeight": FONT_WEIGHT_MEDIUM})
            ], className="d-flex align-items-center")
        ], href=href, active=active, className="nav-link-sidebar")

    else:
        raise ValueError("variant must be 'navbar' or 'sidebar'")