"""District detail page with interactive map and metrics.

This page displays detailed information about a single Prague district, including:
- Interactive map focused on the district
- Safety metrics (police stations)
- Transportation metrics (parking, metro, parking zones)
- Layer toggle controls for map visualization

Users can click info cards to toggle visibility of corresponding map layers.
Layer states are persisted in session storage.
"""
import dash_bootstrap_components as dbc
from dash import register_page, dcc, clientside_callback, Input, Output, html
from src.components.ui.page_heading import page_title
from src.components.pages.district_info import map_section, safety_section, travel_section
from src.components.pages.district_info.accessibility_section import accessibility_section
from src.components.pages.district_info.pr_section import pr_section
from src.components.pages.district_info.environment_section import environment_section
from src.components.pages.district_info.demographics_section import demographics_section
from src.components.pages.district_info.mobility_section import mobility_section
from src.utils.districts.district_utils import get_district_polygons

register_page(__name__, path="/districts/district-detail", name="Detail městské části")

def layout(district=None, lang="cs"):
    """Generate the layout for the district detail page.

    Args:
        district: Name of the district to display (e.g., "Praha 1"). Passed
            as URL query parameter. Defaults to None.
        lang: Language code ("cs" or "en"). Passed as URL query parameter.

    Returns:
        dbc.Container: Complete page layout with stores, map, and metric sections.
    """
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
