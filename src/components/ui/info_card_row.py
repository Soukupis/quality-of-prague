import dash_bootstrap_components as dbc
from dash import html

def info_card_row(cards, col_width=2):
    return dbc.Row([
        html.Div([card for card in cards], className="gap-4 justify-content-start mb-3 d-flex flex-wrap")
    ], className="g-2 justify-content-start mb-3 flex")

def section_header(title, accent_color, bg_color, text_color):
    return html.Div(
        html.H4(title, style={
            "margin": 0,
            "fontWeight": 700,
            "fontSize": "1.25rem",
            "color": text_color,
            "letterSpacing": "0.01em",
        }),
        style={
            "background": bg_color,
            "borderLeft": f"5px solid {accent_color}",
            "borderRadius": "0 0.5rem 0.5rem 0",
            "padding": "0.75rem 1.1rem",
            "marginBottom": "1.25rem",
            "marginTop": "0",
        }
    )

