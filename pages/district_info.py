import dash_bootstrap_components as dbc
from dash import html, register_page, dcc

from components.ui.info_card import info_card
from data_config import DATA_PATHS
from utils.data_loader import read_file
from utils.geospatial_utils import extract_polygons, polygon_points_count, point_count_for_polygon

register_page(__name__, path="/districts/district-detail", name="Districts Detail")

def layout(district=None, **kwargs):
    districts = read_file(DATA_PATHS.prague_districts)
    police_stations = read_file(DATA_PATHS.police_stations)

    polygons = extract_polygons(districts, "geometry", "nazev_1")
    police_station_count = point_count_for_polygon(polygons[district], police_stations, "geometry")

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1(district, className="text-center")
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col(
                info_card("fa-building-shield", "Police stations", police_station_count, "info"), width=3
            ),
        ])
    ], fluid=True, className="py-1")
