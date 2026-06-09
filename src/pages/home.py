import dash_bootstrap_components as dbc
from dash import html, register_page
from src.components.ui import page_title
from src.i18n import t

register_page(__name__, path="/", name="Domů")

_NAV_CARD_KEYS = [
    ("fa-chart-simple",  "nav_dashboard",  "home_card_dashboard_title",  "home_card_dashboard_desc",  "/dashboard", "#667eea"),
    ("fa-location-dot",  "nav_districts",  "home_card_districts_title",  "home_card_districts_desc",  "/districts", "#0ea5e9"),
    ("fa-ranking-star",  "nav_qol_index",  "home_card_qol_title",        "home_card_qol_desc",        "/qol-index", "#f59e0b"),
    ("fa-people-roof",   "nav_personas",   "home_card_personas_title",   "home_card_personas_desc",   "/personas",  "#be185d"),
    ("fa-book-open",     "nav_theory",     "home_card_theory_title",     "home_card_theory_desc",     "/theory",    "#764ba2"),
    ("fa-database",      "nav_datasets",   "home_card_datasets_title",   "home_card_datasets_desc",   "/datasets",  "#0f766e"),
]


def _nav_card(icon_class, title, description, href, color, lang):
    href_with_lang = f"{href}?lang={lang}" if lang != "cs" else href
    return html.A(
        dbc.Card(
            dbc.CardBody([
                html.I(
                    className=f"fa-solid {icon_class}",
                    style={"fontSize": "2rem", "color": color, "marginBottom": "0.65rem", "display": "block"},
                ),
                html.H5(title, style={"fontWeight": "700", "fontSize": "1rem", "color": "#1e293b", "marginBottom": "0.4rem"}),
                html.P(description, style={"fontSize": "0.84rem", "color": "#64748b", "lineHeight": "1.45", "marginBottom": 0}),
            ], className="text-center"),
            className="h-100 hover-shadow",
            style={
                "border": f"1px solid {color}28",
                "borderRadius": "1rem",
                "background": f"linear-gradient(135deg, {color}0f 0%, white 100%)",
                "transition": "all 0.2s ease",
                "cursor": "pointer",
            }
        ),
        href=href_with_lang,
        style={"textDecoration": "none"},
    )


def layout(lang="cs"):
    cards = [
        _nav_card(icon_class, t(title_key, lang), t(desc_key, lang), href, color, lang)
        for icon_class, _, title_key, desc_key, href, color in _NAV_CARD_KEYS
    ]

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                page_title(
                    t("home_title", lang),
                    align="center",
                    description=t("home_desc", lang),
                    use_gradient=True,
                ),
                dbc.Row([
                    dbc.Col(card, xs=12, sm=6, md=4, className="mb-4")
                    for card in cards
                ], className="g-3"),
            ], width=12, lg=10, className="mx-auto"),
        ]),
    ], fluid=True, className="py-4")
