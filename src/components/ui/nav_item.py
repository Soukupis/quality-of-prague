"""Navigation item component with icon support.

This module provides navigation link components for both navbar and sidebar
contexts, with consistent styling and icon support.
"""
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
    """Create a navigation item with icon for navbar or sidebar.

    Builds a styled navigation link component with a Bootstrap icon. Supports
    two variants: compact navbar style and expanded sidebar style. Handles
    active state for current page highlighting.

    Args:
        label: Text label for the navigation item.
        href: URL or path for the link destination.
        icon_name: Bootstrap icon name (without 'bi-' prefix).
        variant: Layout variant - "navbar" for top navigation or "sidebar"
            for side navigation. Defaults to "navbar".
        active: Active state behavior. Can be "exact" (match exact URL),
            "partial" (match URL prefix), True, False, or None. Defaults to
            "exact".
        icon_size: Font size for the icon. Defaults to ICON_SIZE_SMALL.
        icon_color: Color for the icon. Defaults to PRIMARY_COLOR.

    Returns:
        Union[dbc.NavItem, dbc.NavLink]: dbc.NavItem for navbar variant,
            dbc.NavLink for sidebar variant.

    Raises:
        ValueError: If variant is not "navbar" or "sidebar".

    Examples:
        >>> # Navbar item
        >>> item = nav_item(
        ...     label="Dashboard",
        ...     href="/dashboard",
        ...     icon_name="bar-chart",
        ...     variant="navbar"
        ... )
        >>>
        >>> # Sidebar item
        >>> item = nav_item(
        ...     label="Districts",
        ...     href="/districts",
        ...     icon_name="map",
        ...     variant="sidebar",
        ...     active="partial"
        ... )
    """
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