import os
from typing import Dict, Any

class Config:
    # === ENVIRONMENT & DEBUG SETTINGS ===
    # Controls debug mode - enables auto-reload and detailed error messages
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Flask/Dash server host and port settings
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8050))

    # === DATA & CACHING CONFIGURATION ===
    # Cache timeout in seconds for data loading operations
    CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", 300))

    # Cache type configuration for Flask-Caching
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")

    # Data directory path
    DATA_DIR = os.getenv("DATA_DIR", "data")

    # === UI & THEME CONFIGURATION ===
    # Bootstrap theme for dash-bootstrap-components
    # Available themes: BOOTSTRAP, CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, etc.
    BOOTSTRAP_THEME = os.getenv("BOOTSTRAP_THEME", "BOOTSTRAP")

    # App title and branding
    APP_TITLE = os.getenv("APP_TITLE", "Quality of Prague")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Prague Quality of Life Dashboard")

    # === PERFORMANCE SETTINGS ===
    # Suppress callback exceptions for better page routing
    SUPPRESS_CALLBACK_EXCEPTIONS = True

    # Asset settings
    ASSETS_FOLDER = "assets"
    ASSETS_URL_PATH = "/assets/"

    @classmethod
    def get_cache_config(cls) -> Dict[str, Any]:
        return {
            'CACHE_TYPE': cls.CACHE_TYPE,
            'CACHE_DEFAULT_TIMEOUT': cls.CACHE_TIMEOUT
        }

    @classmethod
    def get_bootstrap_theme_url(cls) -> str:
        import dash_bootstrap_components as dbc
        theme_map = {
            'BOOTSTRAP': dbc.themes.BOOTSTRAP,
            'CERULEAN': dbc.themes.CERULEAN,
            'COSMO': dbc.themes.COSMO,
            'CYBORG': dbc.themes.CYBORG,
            'DARKLY': dbc.themes.DARKLY,
            'FLATLY': dbc.themes.FLATLY,
            'JOURNAL': dbc.themes.JOURNAL,
            'LITERA': dbc.themes.LITERA,
            'LUMEN': dbc.themes.LUMEN,
            'LUX': dbc.themes.LUX,
            'MATERIA': dbc.themes.MATERIA,
            'MINTY': dbc.themes.MINTY,
            'MORPH': dbc.themes.MORPH,
            'PULSE': dbc.themes.PULSE,
            'QUARTZ': dbc.themes.QUARTZ,
            'SANDSTONE': dbc.themes.SANDSTONE,
            'SIMPLEX': dbc.themes.SIMPLEX,
            'SKETCHY': dbc.themes.SKETCHY,
            'SLATE': dbc.themes.SLATE,
            'SOLAR': dbc.themes.SOLAR,
            'SPACELAB': dbc.themes.SPACELAB,
            'SUPERHERO': dbc.themes.SUPERHERO,
            'UNITED': dbc.themes.UNITED,
            'VAPOR': dbc.themes.VAPOR,
            'YETI': dbc.themes.YETI,
            'ZEPHYR': dbc.themes.ZEPHYR
        }
        return theme_map.get(cls.BOOTSTRAP_THEME, dbc.themes.BOOTSTRAP)
