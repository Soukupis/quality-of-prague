from dash import html
import dash_bootstrap_components as dbc

def info_card(icon=None, title="", value="", variant=None, card_id=None, dataset_key=None):
    base_class = "info-card"
    variant_class = f"info-card-{variant}" if variant else ""
    card_class = f"{base_class} {variant_class}".strip()

    if card_id:
        card_class += " info-card-clickable"

    # Use pattern-matching IDs if dataset_key is provided, otherwise use simple string IDs
    if dataset_key:
        plus_icon_id = {'type': 'layer-plus-icon', 'index': dataset_key}
        minus_icon_id = {'type': 'layer-minus-icon', 'index': dataset_key}
    else:
        plus_icon_id = f"{card_id}-plus-icon" if card_id else None
        minus_icon_id = f"{card_id}-minus-icon" if card_id else None

    card = dbc.Card(
        dbc.CardBody(
            html.Div([
                html.Div([
                    html.I(
                        id=plus_icon_id,
                        className="fa-solid fa-square-plus info-card-toggle-icon",
                        style={"display": "block"} if card_id else {"display": "none"}
                    ),
                    html.I(
                        id=minus_icon_id,
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
        wrapper_id = {'type': 'layer-card', 'index': dataset_key} if dataset_key else card_id

        return html.Div(
            card,
            id=wrapper_id,
            n_clicks=0,
            style={"cursor": "pointer"}
        )

    return card

