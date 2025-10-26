from .theme import *

NAVBAR_HEIGHT = 70

NAVBAR_STYLE = {
    "height": f"{NAVBAR_HEIGHT}px",
    "background": GRADIENT_LIGHT,
    "backdropFilter": "blur(10px)",
    "borderBottom": "1px solid rgba(0,0,0,0.05)"
}

SIDEBAR_WIDTH = "18rem"

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": NAVBAR_HEIGHT,
    "left": 0,
    "bottom": 0,
    "width": SIDEBAR_WIDTH,
    "padding": f"{SPACING_XL} 0",
    "background": GRADIENT_VERTICAL,
    "borderRight": "1px solid rgba(0,0,0,0.08)",
    "boxShadow": SHADOW_HEAVY,
    "zIndex": 1000,
}

CONTENT_STYLE = {
    "marginLeft": SIDEBAR_WIDTH,
    "marginTop": f"{NAVBAR_HEIGHT}px",
    "padding": SPACING_XL,
    "background": BACKGROUND_COLOR,
    "minHeight": f"calc(100vh - {NAVBAR_HEIGHT}px)",
}

NAV_ITEMS = [
    {
        "label": "Home",
        "href": "/",
        "icon": "house-door"
    },
    {
        "label": "Dashboard",
        "href": "/dashboard",
        "icon": "graph-up"
    },
    {
        "label": "About",
        "href": "/about",
        "icon": "info-circle"
    }
]

BRAND_CONFIG = {
    "text": "Quality of Prague",
    "image_src": "/assets/prague_icon.png",
    "href": "/",
    "text_color": TEXT_COLOR
}
