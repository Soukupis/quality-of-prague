"""District selection component for dashboard page.

This module provides a multi-select dropdown for choosing Prague districts
to compare on the dashboard, with a "Select All" button for convenience.
"""
import dash_bootstrap_components as dbc
from dash import dcc, html
from src.utils.districts.district_utils import get_district_polygons

districts = list(get_district_polygons().keys())
district_options = [{"label": district, "value": district} for district in sorted(districts)]

def district_select():
    """Create the district selection card component.

    Builds a styled card containing a multi-select dropdown for Prague districts
    and a "Select All" button. The dropdown is populated with all available
    districts from the district polygons data.

    Returns:
        dbc.Card: Bootstrap Card component containing the district selection
            dropdown (id: "districts-dropdown") and select all button
            (id: "select-all-districts-btn").

    Examples:
        >>> selector = district_select()
        >>> # Contains dropdown with all Prague districts
        >>> # User can select multiple districts for comparison
    """
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