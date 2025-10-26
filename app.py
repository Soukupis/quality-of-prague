#TODO: creates Dash instance

from dash import Dash, html
import dash_bootstrap_components as dbc
import dash
from callbacks import register_all_callbacks
from components import navbar, sidebar, CONTENT_STYLE
from config import Config
from utils.data_loader import init_cache

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css",
        "/assets/global.css"
    ],
    assets_folder="assets",
    assets_url_path="/assets/"
)

app._favicon = "/assets/favicon.ico"

#register_all_callbacks(app)
init_cache(app)

app.title = "Quality of Prague"

app.layout = html.Div([
    navbar,
    sidebar,
    html.Div(
        dash.page_container,
        style=CONTENT_STYLE
    )
])

if __name__ == "__main__":
    app.run(debug=True)