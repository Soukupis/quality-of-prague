"""Top navigation bar component for the application.

This module provides the main navbar component with branding,
appearing at the top of all pages with fixed positioning.
"""
import dash_bootstrap_components as dbc

from src.components.ui import brand
from src.components.config import NAVBAR_STYLE, BRAND_CONFIG

def navbar():
    """Create the top navigation bar component.

    Builds the main application navbar with branding. The navbar is fixed to
    the top of the viewport and spans the full width. Uses Bootstrap styling
    with custom configuration.

    Returns:
        dbc.Navbar: Bootstrap Navbar component with brand logo/text, styled
            with light theme and shadow effects.

    Examples:
        >>> nav = navbar()
        >>> # nav is a fixed-top navbar with brand
        >>> layout = html.Div([nav, page_content])
    """
    return dbc.Navbar(
    dbc.Container([
        brand(**BRAND_CONFIG),
    ], fluid=True, className="px-4"),
    color="light",
    fixed="top",
    className="shadow-sm border-0",
    style=NAVBAR_STYLE,
)
