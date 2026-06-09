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

    Builds a full-width section header band with a colored left accent stripe
    and a tinted background. Used to visually anchor each district page section.

    Args:
        title: Header text to display.
        accent_color: CSS color for the vertical accent stripe on the left.
        bg_color: CSS color for the header band background.
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
    return html.Div(
        html.H5(title, style={
            "margin": 0,
            "fontWeight": 700,
            "fontSize": "1rem",
            "color": text_color,
            "letterSpacing": "0.01em",
        }),
        style={
            "background": bg_color,
            "borderLeft": f"4px solid {accent_color}",
            "borderRadius": "0 0.5rem 0.5rem 0",
            "padding": "0.5rem 0.85rem",
            "marginBottom": "1rem",
            "marginTop": "0",
        }
    )

