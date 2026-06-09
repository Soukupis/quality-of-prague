from dash import html
from .icon import icon

def page_title(title, icon_name=None, align: str=None, description: str=None, use_gradient: bool=False):
    if use_gradient:
        title_element = html.H1(
            title,
            className="text-center" if align == "center" else "",
            style={
                "fontSize": "4rem",
                "fontWeight": "800",
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "WebkitBackgroundClip": "text",
                "WebkitTextFillColor": "transparent",
                "backgroundClip": "text",
                "marginBottom": "1rem",
                "marginTop": "2rem",
                "letterSpacing": "-1px",
                "textAlign": align
            }
        )
    elif icon_name:
        title_element = html.Div([
            html.Div([
                icon(icon_name, class_name="mb-2", size="3.5rem", style={"color": "#667eea"}),
            ], className="text-center"),
            html.H1(
                title,
                className="text-center mb-0",
                style={
                    "fontWeight": "700",
                    "fontSize": "3rem",
                    "lineHeight": 1.2,
                    "color": "#2c3e50",
                    "letterSpacing": "-0.5px"
                }
            )
        ], style={"marginBottom": "1.5rem", "marginTop": "2rem"})
    else:
        title_element = html.H1(
            title,
            className="display-5 text-center",
            style={
                "fontWeight": 700,
                "fontSize": "3rem",
                "textAlign": align,
                "color": "#2c3e50",
                "marginTop": "2rem",
                "marginBottom": "1.5rem",
                "letterSpacing": "-0.5px"
            }
        )

    if description:
        return html.Div([
            title_element,
            html.P(
                description,
                className="text-center",
                style={
                    "fontSize": "1.2rem",
                    "color": "#6c757d",
                    "fontWeight": "400",
                    "marginBottom": "3rem",
                    "lineHeight": "1.6",
                    "maxWidth": "700px",
                    "margin": "0 auto 3.5rem auto"
                }
            ),
        ], style={"marginBottom": "2rem"})

    return title_element

def page_subtitle(subtitle):
    return html.P(subtitle,className="lead mb-3", style={"fontSize": "1.1rem"})

def page_divider():
    return html.Hr(className="mb-3")