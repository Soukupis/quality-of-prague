import dash_bootstrap_components as dbc
from dash import register_page, dcc, clientside_callback, Input, Output, html
from src.components.ui.page_heading import page_title
from src.components.pages.district_info import map_section, safety_section, travel_section
from src.utils.districts.district_utils import get_district_polygons

register_page(__name__, path="/districts/district-detail", name="Detail městské části")

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
                page_title(district, align="center", use_gradient=True),
                map_section(district, None, None),
                html.Hr(className="my-4"),
                safety_section(district, polygons),
                travel_section(district, polygons),
            ], width=12)
        ]),
    ], fluid=True, className="py-2")

clientside_callback(
    """
    function(district) {
        if (district) {
            document.title = district;
        } else {
            document.title = "Detail městské části - Kvalita Prahy";
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output('district-store', 'id'),
    Input('district-store', 'data')
)
