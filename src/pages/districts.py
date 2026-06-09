import dash_bootstrap_components as dbc
from dash import html, register_page, dcc
from src.components.graphs import create_prague_map
from src.components.ui import page_title
from src.i18n import t

register_page(__name__, path="/districts", name="Městské části")

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
            style={"width": "100%"}
        )
    ], style={"width": "100%"})

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
