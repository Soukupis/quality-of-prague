"""Homepage — entry point for the Quality of Prague application.

A clean welcome screen that orients the user and provides direct navigation
to each major section. No data, no charts — just context and entry points.
"""
import dash_bootstrap_components as dbc
from dash import html, register_page
from src.components.ui import page_title

register_page(__name__, path="/", name="Domů")

_NAV_CARDS = [
    (
        "fa-chart-simple", "Dashboard",
        "Přehled QoL skóre přes celou Prahu — choroplethová mapa, žebříček obvodů a porovnání metrik.",
        "/dashboard", "#667eea",
    ),
    (
        "fa-location-dot", "Městské části",
        "Interaktivní mapa Prahy. Kliknutím na obvod zobrazíte detail s daty ze sedmi domén.",
        "/districts", "#0ea5e9",
    ),
    (
        "fa-ranking-star", "QoL Index",
        "Kompozitní skóre čtyř QOUL domén: bezpečnost, mobilita, přístupnost a prostředí.",
        "/qol-index", "#f59e0b",
    ),
    (
        "fa-people-roof", "Persony",
        "Stejná data, jiné potřeby. Pohled na Prahu očima Jana, Eleny a Rodiny Novákových.",
        "/personas", "#be185d",
    ),
    (
        "fa-book-open", "Teorie",
        "Teoretický rámec: WHOQOL, QOUL 4 domény, 15minutové město a Stiglitz-Sen-Fitoussi.",
        "/theory", "#764ba2",
    ),
    (
        "fa-database", "Datové sady",
        "Dokumentace všech datových zdrojů — původ, formát a popis každého datasetu.",
        "/datasets", "#0f766e",
    ),
]


def _nav_card(icon_class, title, description, href, color):
    return html.A(
        dbc.Card(
            dbc.CardBody([
                html.I(
                    className=f"fa-solid {icon_class}",
                    style={
                        "fontSize": "2rem",
                        "color": color,
                        "marginBottom": "0.65rem",
                        "display": "block",
                    }
                ),
                html.H5(
                    title,
                    style={
                        "fontWeight": "700",
                        "fontSize": "1rem",
                        "color": "#1e293b",
                        "marginBottom": "0.4rem",
                    }
                ),
                html.P(
                    description,
                    style={
                        "fontSize": "0.84rem",
                        "color": "#64748b",
                        "lineHeight": "1.45",
                        "marginBottom": 0,
                    }
                ),
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
        href=href,
        style={"textDecoration": "none"},
    )


layout = dbc.Container([
    dbc.Row([
        dbc.Col([

            page_title(
                "Quality of Prague",
                align="center",
                description=(
                    "Otevřená data o kvalitě života ve 57 pražských obvodech — "
                    "bezpečnost, mobilita, přístupnost a prostředí."
                ),
                use_gradient=True,
            ),

            dbc.Row([
                dbc.Col(_nav_card(*card), xs=12, sm=6, md=4, className="mb-4")
                for card in _NAV_CARDS
            ], className="g-3"),

        ], width=12, lg=10, className="mx-auto"),
    ]),
], fluid=True, className="py-4")
