import dash_bootstrap_components as dbc
from dash import html, register_page
from src.components.ui import page_title, page_subtitle, page_divider, feature_card

register_page(__name__, path="/", name="Domů")

feature_cards = dbc.Row([
    dbc.Col([
        feature_card(
            icon_name="bar-chart",
            title="Dashboard",
            description="Interaktivní poznatky a metriky o kvalitě života v Praze.",
            button_text="Dashboard",
            button_href="/dashboard"
        )
    ], md=3, xs=12, className="mb-4"),
    dbc.Col([
        feature_card(
            icon_name="geo-alt",
            title="Městské části",
            description="Prozkoumejte ukazatele kvality života napříč pražskými městskými částmi.",
            button_text="Městské části",
            button_href="/districts"
        )
    ], md=3, xs=12, className="mb-4"),
    dbc.Col([
        feature_card(
            icon_name="database",
            title="Datové sady",
            description="Procházejte datasety, které stojí za analytikou a vizualizacemi.",
            button_text="Datové sady",
            button_href="/datasets"
        )
    ], md=3, xs=12, className="mb-4"),
    dbc.Col([
        feature_card(
            icon_name="info-circle",
            title="O Aplikaci",
            description="Zjistěte více o účelu a pozadí této platformy.",
            button_text="O Aplikaci",
            button_href="/about"
        )
    ], md=3, xs=12, className="mb-4"),
], className="g-4 justify-content-center")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            page_title("Quality of Prague"),
            page_subtitle("Platforma pro analýzu a prezentaci ukazatelů kvality života v Praze."),
            page_divider(),
            html.P(
                "Prozkoumejte dashboard pro získání poznatků, zjistěte více o projektu, zobrazte městské části nebo procházejte dostupné datasety.",
                className="mb-4",
                style={"fontSize": "1.05rem"}
            ),
            feature_cards
        ], width=12)
    ])
], fluid=True, className="py-2")
