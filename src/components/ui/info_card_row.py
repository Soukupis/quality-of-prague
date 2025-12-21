"""Info card layout and section header components.

This module provides layout utilities for organizing info cards into responsive
rows and creating styled section headers with accent colors.
"""
import dash_bootstrap_components as dbc
from dash import html

def info_card_row(cards, col_width=2):
    """Create a responsive row layout for info cards.

    Arranges a list of info card components into a flexbox row with gap spacing
    and wrapping behavior for responsive display.

    Args:
        cards: List of info card components to display in the row.
        col_width: Bootstrap column width (1-12). Not currently used in
            implementation but reserved for future grid layout. Defaults to 2.

    Returns:
        dbc.Row: Bootstrap Row containing the cards in a flexbox layout with
            gap spacing and wrapping.

    Examples:
        >>> from src.components.ui import info_card
        >>> cards = [
        ...     info_card(icon="fa-parking", title="Parking", value="123"),
        ...     info_card(icon="fa-subway", title="Metro", value="45")
        ... ]
        >>> row = info_card_row(cards, col_width=3)
    """
    return dbc.Row([
        html.Div([card for card in cards], className="gap-4 justify-content-start mb-3 d-flex flex-wrap")
    ], className="g-2 justify-content-start mb-3 flex")

def section_header(title, accent_color, bg_color, text_color):
    """Create a styled section header with accent color stripe.

    Builds a section header with a colored vertical accent stripe on the left
    and a background-colored title area. Used to visually separate different
    sections on a page.

    Args:
        title: Header text to display.
        accent_color: CSS color for the vertical accent stripe on the left.
        bg_color: CSS color for the title background.
        text_color: CSS color for the title text.

    Returns:
        html.Div: Styled header component with accent stripe and title.

    Examples:
        >>> from src.components.config import theme
        >>> header = section_header(
        ...     title="Bezpečnost",
        ...     accent_color=theme.SAFETY_ACCENT_COLOR,
        ...     bg_color=theme.SAFETY_BG_COLOR,
        ...     text_color=theme.SAFETY_TEXT_COLOR
        ... )
    """
    return html.Div([
        html.Span("", style={
            "display": "inline-block",
            "width": "5px",
            "height": "22px",
            "background": accent_color,
            "borderRadius": "4px",
            "marginRight": "10px",
            "verticalAlign": "middle"
        }),
        html.H5(title, style={
            "display": "inline-block",
            "background": bg_color,
            "padding": "4px 14px 4px 0",
            "margin": 0,
            "fontWeight": 600,
            "fontSize": "1rem",
            "color": text_color,
            "borderRadius": "0 6px 6px 0"
        })
    ], style={"marginBottom": "8px", "marginTop": "12px"})

