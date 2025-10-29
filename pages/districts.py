import dash_bootstrap_components as dbc
from dash import html, register_page, dcc
from components.graphs import create_prague_map
from components.ui.page_heading import page_title, page_subtitle, page_divider

register_page(__name__, path="/districts", name="Districts")

def create_map_section():
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
        )
    ])

def create_main_grid():
    return html.Div([
        dcc.Location(id="url",  refresh="callback-nav"),
        create_map_section(),
    ], style={
        'maxWidth': '950px',
        'marginLeft': 'auto',
        'marginRight': 'auto',
        'width': '100%'
    })

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            page_title("Districts", icon_name="geo-alt"),
            page_subtitle("Explore various quality of life metrics across different districts in Prague."),
            page_divider(),
            create_main_grid()
        ], width=12)
    ])
], fluid=True, className="py-2")
