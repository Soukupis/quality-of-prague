import dash_bootstrap_components as dbc
from dash import dcc, html
from src.utils.districts.district_utils import get_district_polygons

districts = list(get_district_polygons().keys())
district_options = [{"label": district, "value": district} for district in sorted(districts)]

def district_select():
    return dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div([
                            html.I(className="bi bi-bar-chart", style={"fontSize": "1.5rem", "color": "#667eea", "marginRight": "0.5rem"}),
                            html.Label("Městské části", className="fw-bold mb-0", style={"fontSize": "1.2rem", "color": "#2c3e50"})
                        ], className="d-flex align-items-center"),
                        dbc.Button(
                            "Vybrat vše",
                            id="select-all-districts-btn",
                            size="sm",
                            color="primary",
                            outline=True,
                            className="ms-auto",
                            style={"fontSize": "0.85rem", "borderRadius": "0.5rem"}
                        )
                    ], className="d-flex align-items-center justify-content-between mb-3"),
                    dcc.Dropdown(
                        id="districts-dropdown",
                        options=district_options,
                        multi=True,
                        placeholder="Vyberte městské části...",
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
                "background": "linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%)"
            })