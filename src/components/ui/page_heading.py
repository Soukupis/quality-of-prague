from dash import html
from .icon import icon

def page_title(title, icon_name=None):
    if icon_name:
        return html.Div([
            icon(icon_name, class_name="me-2", size="2.4rem", style={"verticalAlign": "middle", "marginTop": "0.1em"}),
            html.Span(title, className="display-5 mb-0", style={"fontWeight": 700, "fontSize": "2.2rem", "verticalAlign": "middle", "lineHeight": 1})
        ], className="d-flex align-items-center mb-3", style={"lineHeight": 1})
    else:
        return html.H1(title, className="display-5 mb-4", style={"fontWeight": 700, "fontSize": "2.2rem"})

def page_subtitle(subtitle):
    return html.P(subtitle,className="lead mb-3", style={"fontSize": "1.1rem"})

def page_divider():
    return html.Hr(className="mb-3")