import dash_bootstrap_components as dbc
from dash import dcc, html
from src.configs.data_config import DATA_PATHS


def data_select():
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className="bi bi-geo-alt",
                       style={"fontSize": "1.5rem", "color": "#764ba2", "marginRight": "0.5rem"}),
                html.Label("Data", className="fw-bold mb-0", style={"fontSize": "1.2rem", "color": "#2c3e50"})
            ], className="d-flex align-items-center mb-3"),
            dcc.Dropdown(
                id="data-dropdown",
                options=DATA_PATHS.get_dataset_value_options(),
                placeholder="Vyberte data...",
                className="custom-dropdown",
                style={
                    "fontSize": "1rem",
                    "borderRadius": "0.5rem"
                }
            )
        ])
    ], className="shadow-sm h-100", style={
        "border": "none",
        "borderRadius": "1rem",
        "background": "linear-gradient(135deg, #fff8f9 0%, #ffffff 100%)"
    })