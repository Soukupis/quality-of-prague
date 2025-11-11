import dash_bootstrap_components as dbc

def info_card_row(cards, col_width=2):
    return dbc.Row([
        html.Div([card for card in cards], className="gap-4 justify-content-start mb-3 d-flex")
    ], className="g-2 justify-content-start mb-3 flex")
from dash import html

def section_header(title, accent_color, bg_color, text_color):
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

