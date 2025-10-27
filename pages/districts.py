import dash_bootstrap_components as dbc
from dash import html, register_page
from dash import dcc
from components.graphs import create_prague_map

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
            html.H1("Districts of Prague", className="display-4 mb-5 text-center"),
            create_main_grid()
        ], width=12)
    ])
], fluid=True, className="py-1")
