import dash_bootstrap_components as dbc
from dash import html, register_page, dcc
from components.graphs.maps.districts import create_single_district_map
from components.ui.info_card import info_card
from components.ui.info_card_row import info_card_row, section_header
from components.ui.page_heading import page_title, page_divider
from components.config import theme
from utils.districts.district_utils import get_district_polygons
from utils.geospatial_utils import point_count_for_polygon
from utils.loaders.districts_loader import get_police_stations_data, get_parking_meters_data

register_page(__name__, path="/districts/district-detail", name="Districts Detail")

def heading(title):
    return dbc.Row([
        dbc.Col([
            html.H2(title, className="text-center mb-4", style={"fontWeight": "bold", "fontSize": "2.2rem"})
        ], width=12)
    ])

def create_map_section(district: str = None, scatters = None):
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
                info_card("fa-building-shield", "Police stations", police_station_count, "info", card_id="police-stations")
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
                info_card("fa-parking", "Parking meters", parking_meters_count, "info", card_id="parking-meters")
            ], col_width=2)
        ], width=12)
    ])

def layout(district=None, **kwargs):
    # Use cached loaders - loaders is loaded once and reused
    police_stations = get_police_stations_data()
    parking_meters = get_parking_meters_data()
    polygons = get_district_polygons()

    police_station_count = point_count_for_polygon(polygons[district], police_stations, "geometry")
    parking_meters_count = point_count_for_polygon(polygons[district], parking_meters, "geometry")

    # Start with empty map - layers will appear when cards are clicked
    return dbc.Container([
        dcc.Store(id='district-store', data=district),
        dcc.Store(
            id='visible-layers-store',
            data=[],
            storage_type='session'
        ),
        dbc.Row([
            dbc.Col([
                page_title(district, icon_name="geo-alt"),
                page_divider(),
                create_map_section(district, None),
                page_divider(),
                safety_section(police_station_count),
                travel_section(parking_meters_count),
            ], width=12)
        ]),
    ], fluid=True, className="py-2")