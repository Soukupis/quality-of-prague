import dash_bootstrap_components as dbc

def category_card(title, children, header_bg="#f5f7fa", header_color="#222", header_border=None, card_class="shadow-sm mb-4 rounded-4 border-0 bg-light", header_style=None):
    style = {
        "background": header_bg,
        "color": header_color,
        "fontWeight": "600",
        "fontSize": "1.2rem",
        "borderTopLeftRadius": ".5rem",
        "borderTopRightRadius": ".5rem",
    }
    if header_border:
        style["borderBottom"] = header_border
    if header_style:
        style.update(header_style)
    return dbc.Card([
        dbc.CardHeader(title, style=style),
        dbc.CardBody(children)
    ], className=card_class)

