"""Districts overview page with interactive Prague map.

This page displays an interactive map of all Prague districts. Users can click
on districts to navigate to detailed district information pages. The map shows
all districts with choropleth visualization and district labels.
"""
import dash_bootstrap_components as dbc
from dash import html, register_page, dcc
from src.components.graphs import create_prague_map
from src.components.ui import page_title
from src.i18n import t

register_page(__name__, path="/districts", name="Městské části")

def create_map_section():
    """Create the interactive map section for the districts page.

    Returns:
        html.Div: Container with the Prague districts map configured for
            click interactions and navigation.
    """
    return html.Div([
        dcc.Graph(
            id="prague-map",
            figure=create_prague_map(),
            config={
                'displayModeBar': False,
                'scrollZoom': False,
                'doubleClick': 'reset',
                'responsive': True
            },
            style={"width": "100%"}
        )
    ], style={"width": "100%"})

def create_main_grid():
    """Create the main content grid for the districts page.

    Builds the central layout containing the URL location component and the
    interactive map section. The grid is centered with a maximum width for
    optimal viewing on different screen sizes.

    Returns:
        html.Div: Main content container with URL location and map section,
            centered with max-width of 950px.

    Examples:
        >>> grid = create_main_grid()
        >>> # grid contains dcc.Location and map section
        >>> # Used in the main page layout
    """
    return html.Div([
        dcc.Location(id="url",  refresh="callback-nav"),
        create_map_section(),
    ], style={
        'maxWidth': '950px',
        'marginLeft': 'auto',
        'marginRight': 'auto',
        'width': '100%'
    })

def layout(lang="cs"):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                page_title(
                    t("districts_title", lang),
                    align="center",
                    description=t("districts_desc", lang),
                    use_gradient=True,
                ),
                create_main_grid(),
            ], width=12)
        ])
    ], fluid=True, className="py-2")
