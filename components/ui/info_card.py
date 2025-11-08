from dash import html
import dash_bootstrap_components as dbc

def info_card(icon=None, title="", value="", variant=None, card_id=None):
    base_class = "info-card"
    variant_class = f"info-card-{variant}" if variant else ""
    card_class = f"{base_class} {variant_class}".strip()

    if card_id:
        card_class += " info-card-clickable"

    card = dbc.Card(
        dbc.CardBody(
            html.Div([
                html.I(className=f"fa-solid {icon} info-card-icon me-2") if icon else None,
                html.H4(title, className="info-card-title mb-0 me-2"),
                html.Span(value, className="info-card-number ms-2")
            ], className="d-flex align-items-center justify-content-start gap-2")
        ),
        className=card_class,
    )

    if card_id:
        return html.Div(
            card,
            id=card_id,
            n_clicks=0,
            style={"cursor": "pointer"}
        )

    return card

