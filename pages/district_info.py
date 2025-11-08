import dash_bootstrap_components as dbc
from dash import register_page, dcc
from components.ui.page_heading import page_title, page_divider
from components.pages.district_info import map_section, safety_section, travel_section
from utils.districts.district_utils import get_district_polygons

register_page(__name__, path="/districts/district-detail", name="Districts Detail")

def layout(district=None):
    polygons = get_district_polygons()

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
                map_section(district, None),
                page_divider(),
                safety_section(district, polygons),
                travel_section(district, polygons),
            ], width=12)
        ]),
    ], fluid=True, className="py-2")