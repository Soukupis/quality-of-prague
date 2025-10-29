import dash_bootstrap_components as dbc
from dash import html, register_page, dcc

from components.ui.info_card import info_card
from components.ui.info_card_row import info_card_row, section_header
from data_config import DATA_PATHS
from utils.data_loader import read_file
from utils.geospatial_utils import extract_polygons, polygon_points_count, point_count_for_polygon
from components.config import theme

register_page(__name__, path="/districts/district-detail", name="Districts Detail")

def heading(title):
    return dbc.Row([
        dbc.Col([
            html.H2(title, className="text-center mb-4", style={"fontWeight": "bold", "fontSize": "2.2rem"})
        ], width=12)
    ])

def safety_section(police_station_count):
    return dbc.Row([
        dbc.Col([
            section_header(
                title="Safety",
                accent_color=theme.SAFETY_ACCENT_COLOR,
                bg_color=theme.SAFETY_BG_COLOR,
                text_color=theme.SAFETY_TEXT_COLOR
            ),
            info_card_row([
                info_card("fa-building-shield", "Police stations", police_station_count, "info")
            ], col_width=2)
        ], width=12)
    ])

def travel_section(parking_meters_count):
    return dbc.Row([
        dbc.Col([
            section_header(
                title="Travel",
                accent_color=theme.TRAVEL_ACCENT_COLOR,
                bg_color=theme.TRAVEL_BG_COLOR,
                text_color=theme.TRAVEL_TEXT_COLOR
            ),
            info_card_row([
                info_card("fa-parking", "Parking meters", parking_meters_count, "info")
            ], col_width=2)
        ], width=12)
    ])

def layout(district=None, **kwargs):
    districts = read_file(DATA_PATHS.prague_districts)
    police_stations = read_file(DATA_PATHS.police_stations)
    parking_meters = read_file(DATA_PATHS.parking_meters)

    polygons = extract_polygons(districts, "geometry", "nazev_1")
    police_station_count = point_count_for_polygon(polygons[district], police_stations, "geometry")
    parking_meters_count = point_count_for_polygon(polygons[district], parking_meters, "geometry")

    return dbc.Container([
        heading(district),
        safety_section(police_station_count),
        travel_section(parking_meters_count),
    ], fluid=True, className="py-1")
