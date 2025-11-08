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
                html.Div([
                    html.I(
                        id=f"{card_id}-plus-icon" if card_id else None,
                        className="fa-solid fa-square-plus info-card-toggle-icon",
                        style={"display": "block"} if card_id else {"display": "none"}
                    ),
                    html.I(
                        id=f"{card_id}-minus-icon" if card_id else None,
                        className="fa-solid fa-square-minus info-card-toggle-icon",
                        style={"display": "none"}
                    )
                ]) if card_id else None,
                html.Div(className="info-card-divider") if card_id else None,
                html.I(className=f"fa-solid {icon} info-card-icon") if icon else None,
                html.Div([
                    html.H4(title, className="info-card-title mb-0"),
                    html.Span(value, className="info-card-number")
                ], className="d-flex flex-column flex-sm-row align-items-start align-items-sm-center gap-1 flex-grow-1")
            ], className="d-flex align-items-center justify-content-start gap-2 w-100")
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

