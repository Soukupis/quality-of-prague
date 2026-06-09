from dash import callback, Output, Input, State, ctx


def _set_lang_in_search(pathname: str, search: str, lang: str) -> str:
    """Return a new search string with lang= added/replaced, preserving other params."""
    params = {}
    if search:
        for part in search.lstrip("?").split("&"):
            if "=" in part:
                k, v = part.split("=", 1)
                params[k] = v
    params["lang"] = lang
    return "?" + "&".join(f"{k}={v}" for k, v in params.items())


_ACTIVE_BTN_STYLE = {
    "background": "#667eea",
    "color": "white",
    "border": "1px solid #667eea",
    "borderRadius": "0.35rem",
    "padding": "3px 10px",
    "fontSize": "0.78rem",
    "fontWeight": "700",
    "cursor": "pointer",
    "marginRight": "0.25rem",
    "transition": "all 0.15s",
}
_INACTIVE_BTN_STYLE = {
    "background": "transparent",
    "color": "#94a3b8",
    "border": "1px solid #cbd5e1",
    "borderRadius": "0.35rem",
    "padding": "3px 10px",
    "fontSize": "0.78rem",
    "fontWeight": "700",
    "cursor": "pointer",
    "marginRight": "0.25rem",
    "transition": "all 0.15s",
}


@callback(
    Output("lang-store", "data"),
    Output("lang-nav", "href"),
    Input("btn-lang-cs", "n_clicks"),
    Input("btn-lang-en", "n_clicks"),
    State("app-location", "pathname"),
    State("app-location", "search"),
    prevent_initial_call=True,
)
def switch_language(_cs, _en, pathname, search):
    lang = "cs" if ctx.triggered_id == "btn-lang-cs" else "en"
    new_search = _set_lang_in_search(pathname or "/", search or "", lang)
    return lang, (pathname or "/") + new_search


@callback(
    Output("btn-lang-cs", "style"),
    Output("btn-lang-en", "style"),
    Input("lang-store", "data"),
)
def update_lang_button_styles(lang):
    lang = lang or "cs"
    cs_style = _ACTIVE_BTN_STYLE if lang == "cs" else _INACTIVE_BTN_STYLE
    en_style = _ACTIVE_BTN_STYLE if lang == "en" else _INACTIVE_BTN_STYLE
    return cs_style, en_style


@callback(
    Output("sidebar-nav-container", "children"),
    Input("lang-store", "data"),
)
def update_sidebar_nav(lang):
    """Rebuild sidebar nav items when language changes so hrefs include ?lang=."""
    from src.components.sidebar.sidebar import _render_nav_items
    return _render_nav_items(lang or "cs")
