from dash import html
import dash_bootstrap_components as dbc
from .icon import icon

CARD_BUTTON_GRADIENT = "linear-gradient(135deg, #4A90E2 0%, #357ABD 100%)"


def feature_card(icon_name, title, description, button_text, button_href):
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                icon(icon_name, class_name="me-2", size="2rem"),
                html.H5(title, className="card-title mb-0", style={"fontWeight": 600})
            ], className="d-flex align-items-center gap-2 mb-3"),
            html.P(description, className="card-text mb-4", style={"fontSize": "1.01rem"}),
            html.Div([
                dbc.Button(
                    button_text,
                    href=button_href,
                    className="w-100",
                    style={
                        "background": CARD_BUTTON_GRADIENT,
                        "border": "none",
                        "color": "#fff",
                        "fontWeight": 500
                    }
                )
            ], className="d-flex align-items-end flex-grow-1")
        ], className="d-flex flex-column h-100 justify-content-between")
    ], className="h-100 shadow-sm border-0")