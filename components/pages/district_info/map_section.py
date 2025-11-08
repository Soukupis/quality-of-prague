from dash import html, dcc
from components.graphs import create_single_district_map


def map_section(district: str = None, scatters = None):
    return html.Div([
        dcc.Graph(
            id="single-district-map",
            figure=create_single_district_map(district, scatters),
            config={
                'displayModeBar': False,
            },
            style={"marginBottom": "60px", "width": "100%"}
        )
    ], style={"width": "100%"})