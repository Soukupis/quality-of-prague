import dash_bootstrap_components as dbc
from dash import register_page, dcc, clientside_callback, Input, Output, html
from src.components.ui import page_title
from src.components.pages.district_info import (
    map_section, safety_section, travel_section,
    accessibility_section, pr_section, environment_section,
    demographics_section, mobility_section,
)
from src.utils.districts import get_district_polygons

register_page(__name__, path="/districts/district-detail", name="Detail městské části")

def layout(district=None, lang="cs"):
    polygons = get_district_polygons()

    _sections = [
        safety_section(district, polygons, lang),
        travel_section(district, polygons, lang),
        accessibility_section(district, polygons, lang),
        pr_section(district, polygons, lang),
        mobility_section(district, polygons, lang),
        environment_section(district, polygons, lang),
        demographics_section(district, polygons, lang),
    ]

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
                *[
                    item
                    for i, s in enumerate(s for s in _sections if s is not None)
                    for item in (
                        [html.Hr(style={"borderColor": "#e2e8f0", "margin": "2rem 0"}), html.Div(s, className="mb-4")]
                        if i > 0 else
                        [html.Div(s, className="mb-4")]
                    )
                ],
            ], width=12)
        ]),
    ], fluid=True, className="py-3")

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
