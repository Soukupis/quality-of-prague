from dash import html
import dash_bootstrap_components as dbc

def info_card(icon=None, title="", value="", variant=None):
    base_class = "info-card"
    variant_class = f"info-card-{variant}" if variant else ""
    card_class = f"{base_class} {variant_class}".strip()
    return dbc.Card(
        dbc.CardBody(
            html.Div([
                html.I(className=f"fa-solid {icon} info-card-icon me-2") if icon else None,
                html.H4(title, className="info-card-title mb-0 me-2"),
                html.Span(value, className="info-card-number ms-2")
            ], className="d-flex align-items-center justify-content-start gap-2")
        ),
        className=card_class
    )
