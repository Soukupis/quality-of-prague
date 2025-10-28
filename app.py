#TODO: creates Dash instance

from dash import Dash, html
import dash
from components import navbar, sidebar, CONTENT_STYLE
from config import Config
from utils.data_loader import init_cache

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=Config.SUPPRESS_CALLBACK_EXCEPTIONS,
    external_stylesheets=[
        Config.get_bootstrap_theme_url(),
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css",
        Config.ASSETS_URL_PATH + "global.css"
    ],
    assets_folder=Config.ASSETS_FOLDER,
    assets_url_path=Config.ASSETS_URL_PATH
)
from callbacks import district_map_callbacks


app._favicon = Config.ASSETS_URL_PATH + "favicon.ico"

init_cache(app)

app.title = Config.APP_TITLE

app.layout = html.Div([
    navbar,
    sidebar,
    html.Div(
        dash.page_container,
        style=CONTENT_STYLE
    )
])

if __name__ == "__main__":
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
