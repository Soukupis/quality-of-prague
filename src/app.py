from dash import Dash, html
import dash
from src.components.config import CONTENT_STYLE
from src.configs.config import Config
from src.components.navbar import navbar
from src.components.sidebar import sidebar
from src.utils.cache import init_cache

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=Config.SUPPRESS_CALLBACK_EXCEPTIONS,
    external_stylesheets=[
        Config.get_bootstrap_theme_url(),
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css",
        Config.ASSETS_URL_PATH + "global.css"
    ],
    assets_folder=Config.ASSETS_FOLDER,
    assets_url_path=Config.ASSETS_URL_PATH,
    update_title=None
)
from src.callbacks import district_map_callbacks


init_cache(app)

app.title = Config.APP_TITLE

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    navbar(),
    sidebar(),
    html.Div(
        dash.page_container,
        style=CONTENT_STYLE
    )
])

if __name__ == "__main__":
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
