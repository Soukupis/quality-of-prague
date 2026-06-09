"""About page for the Quality of Prague application.

Provides a rich Czech-language introduction to the application: its purpose,
theoretical background, datasets used, and navigation guide.
"""
import dash_bootstrap_components as dbc
from dash import register_page, html
from src.components.ui import page_title

register_page(__name__, path="/about", name="O Aplikaci")


# ── Shared helpers (mirror of theory.py pattern) ─────────────────────────────

def _section_card(icon_class, title, color, children):
    return dbc.Card([
        dbc.CardHeader(
            html.Div([
                html.I(className=f"fa-solid {icon_class}",
                       style={"fontSize": "1.3rem", "color": color, "marginRight": "0.6rem"}),
                html.Span(title, style={"fontWeight": "700", "fontSize": "1rem", "color": "#1e293b"}),
            ], className="d-flex align-items-center"),
            style={"background": "white", "border": "none", "paddingBottom": "0"}
        ),
        dbc.CardBody(children),
    ], className="shadow-sm mb-4", style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"})


def _framework_mini_card(title, subtitle, items, bg, border, title_color):
    return dbc.Card([
        dbc.CardBody([
            html.Div(title, style={"fontWeight": "700", "fontSize": "0.9rem",
                                   "color": title_color, "marginBottom": "0.2rem"}),
            html.Div(subtitle, style={"fontSize": "0.78rem", "color": "#64748b",
                                      "marginBottom": "0.5rem"}),
            html.Ul([
                html.Li(item, style={"fontSize": "0.8rem", "color": "#475569"})
                for item in items
            ], style={"paddingLeft": "1.1rem", "marginBottom": 0})
        ], style={"padding": "0.75rem 1rem"})
    ], style={"background": bg, "border": f"1px solid {border}",
              "borderRadius": "0.75rem", "height": "100%"})


def _dataset_chip(label):
    return html.Span(
        label,
        style={
            "display": "inline-block",
            "background": "#f0fdf4",
            "color": "#166534",
            "borderRadius": "1rem",
            "padding": "2px 10px",
            "fontSize": "0.82rem",
            "fontWeight": "600",
            "marginRight": "0.4rem",
            "marginBottom": "0.5rem",
        }
    )


def _nav_row(icon_class, page_name, description, color):
    return html.Div([
        html.I(className=f"fa-solid {icon_class}",
               style={"fontSize": "1rem", "color": color,
                      "minWidth": "1.5rem", "marginTop": "2px"}),
        html.Div([
            html.Span(page_name, style={"fontWeight": "700", "fontSize": "0.9rem",
                                        "color": "#1e293b"}),
            html.Span(f" — {description}",
                      style={"fontSize": "0.88rem", "color": "#64748b"}),
        ], style={"marginLeft": "0.6rem"})
    ], className="d-flex align-items-start mb-3")


# ── Section 1: Co je Quality of Prague? ──────────────────────────────────────

intro = _section_card(
    "fa-city", "Co je Quality of Prague?", "#667eea",
    [
        html.P(
            "Quality of Prague je interaktivní dashboard pro analýzu kvality života v městských "
            "částech Prahy. Umožňuje exploraci a porovnání otevřených urbánních dat napříč 57 "
            "pražskými obvody — od bezpečnosti a dopravy po kvalitu ovzduší a přístupnost služeb.",
            style={"fontSize": "0.9rem", "color": "#475569", "lineHeight": "1.6",
                   "marginBottom": "1rem"}
        ),
        html.Div([
            html.Div([
                html.I(className="fa-solid fa-graduation-cap",
                       style={"fontSize": "1.1rem", "color": "#667eea", "marginRight": "0.5rem"}),
                html.Span("Vznik aplikace", style={"fontWeight": "700", "color": "#1e293b"}),
            ], className="d-flex align-items-center mb-2"),
            html.P([
                "Aplikace vznikla jako součást diplomové práce ",
                html.Em(
                    "\"Analýza faktorů ovlivňujících kvalitu života v městském prostředí: "
                    "případová studie Prahy s využitím dat z urbanistického plánování\"",
                    style={"color": "#4f46e5"}
                ),
                " (Bc. Joseph Meurer, Unicorn Vysoká Škola).",
            ], style={"fontSize": "0.88rem", "color": "#475569", "marginBottom": 0}),
        ], style={"background": "#f5f3ff", "borderLeft": "4px solid #667eea",
                  "padding": "0.85rem 1rem", "borderRadius": "0 0.75rem 0.75rem 0",
                  "marginBottom": "1rem"}),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className="fa-solid fa-bullseye",
                           style={"fontSize": "1.5rem", "color": "#667eea",
                                  "marginBottom": "0.4rem"}),
                    html.H6("Cíl", style={"fontWeight": "700", "color": "#1e293b"}),
                    html.P(
                        "Přeložit teoretické modely QoL do navigovatelného nástroje postaveného "
                        "na důkazech — s využitím otevřených urbánních dat.",
                        style={"fontSize": "0.83rem", "color": "#475569", "marginBottom": 0}
                    ),
                ], style={"padding": "0.85rem", "background": "#fafafa",
                          "borderRadius": "0.75rem", "height": "100%",
                          "border": "1px solid #e2e8f0"})
            ], md=4, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.I(className="fa-solid fa-map-location-dot",
                           style={"fontSize": "1.5rem", "color": "#0ea5e9",
                                  "marginBottom": "0.4rem"}),
                    html.H6("Praha — 57 obvodů", style={"fontWeight": "700", "color": "#1e293b"}),
                    html.P(
                        "Pražské městské části se výrazně liší v infrastruktuře, demografii "
                        "i dostupnosti služeb — data tato rozdíly odhalují.",
                        style={"fontSize": "0.83rem", "color": "#475569", "marginBottom": 0}
                    ),
                ], style={"padding": "0.85rem", "background": "#f0f9ff",
                          "borderRadius": "0.75rem", "height": "100%",
                          "border": "1px solid #bae6fd"})
            ], md=4, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.I(className="fa-solid fa-database",
                           style={"fontSize": "1.5rem", "color": "#10b981",
                                  "marginBottom": "0.4rem"}),
                    html.H6("Otevřená data", style={"fontWeight": "700", "color": "#1e293b"}),
                    html.P(
                        "Všechna data pocházejí z veřejně dostupných zdrojů: IPR Praha, "
                        "Geoportál, ČHMÚ, OpenStreetMap a dalších.",
                        style={"fontSize": "0.83rem", "color": "#475569", "marginBottom": 0}
                    ),
                ], style={"padding": "0.85rem", "background": "#f0fdf4",
                          "borderRadius": "0.75rem", "height": "100%",
                          "border": "1px solid #bbf7d0"})
            ], md=4, className="mb-3"),
        ])
    ]
)


# ── Section 2: Teoretický rámec ───────────────────────────────────────────────

theory = _section_card(
    "fa-book-open", "Teoretický rámec", "#764ba2",
    [
        html.P(
            "Dashboard vychází ze čtyř akademicky zakotvených přístupů k měření kvality života. "
            "Každý přináší jiný pohled — od individuální pohody přes urbánní operacionalizaci "
            "až po komisionální doporučení pro národní statistiky.",
            style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1rem",
                   "lineHeight": "1.6"}
        ),
        dbc.Row([
            dbc.Col([
                _framework_mini_card(
                    "WHOQOL (WHO)",
                    "6 domén individuální pohody",
                    [
                        "Fyzická — energie, spánek, bolest",
                        "Psychologická — sebehodnocení, emoce",
                        "Úroveň nezávislosti — pohyblivost",
                        "Sociální vztahy — podpora, komunita",
                        "Prostředí — bezpečnost, doprava, rekreace",
                        "Spiritualita — celkové vnímání",
                    ],
                    "#f0f9ff", "#bae6fd", "#0369a1"
                )
            ], md=6, className="mb-3"),
            dbc.Col([
                _framework_mini_card(
                    "QOUL — 4 operační domény",
                    "Základ analytické struktury dashboardu",
                    [
                        "Socioekonomická bezpečnost",
                        "Mobilita — MHD, intermodalita",
                        "Přístupnost — bezbariérový přístup",
                        "Životní prostředí — ovzduší, zeleň",
                    ],
                    "#f0fdfa", "#99f6e4", "#0f766e"
                )
            ], md=6, className="mb-3"),
            dbc.Col([
                _framework_mini_card(
                    "Město 15 minut (Moreno et al., 2021)",
                    "6 funkcí, 4 dimenze realizace",
                    [
                        "Funkce: bydlení, práce, nákupy, zdraví, vzdělání, volný čas",
                        "Hustota — optimální počet obyvatel / km²",
                        "Blízkost — prostorová i časová dostupnost",
                        "Diverzita — smíšené využití, sociální mix",
                        "Digitalizace — IoT, sdílená kola, big data",
                    ],
                    "#fff1f2", "#fecdd3", "#be123c"
                )
            ], md=6, className="mb-3"),
            dbc.Col([
                _framework_mini_card(
                    "Stiglitz-Sen-Fitoussi Commission",
                    "Objektivní ukazatele vs. subjektivní pohoda",
                    [
                        "Oddělení objektivních měření od subjektivního prožitku",
                        "Doporučení pro národní statistiky (2009)",
                        "\"Samotné podmínky nestačí — vnímání hraje klíčovou roli\"",
                        "Základ pro dvouvrstvý přístup v tomto dashboardu",
                    ],
                    "#faf5ff", "#e9d5ff", "#7c3aed"
                )
            ], md=6, className="mb-3"),
        ])
    ]
)


# ── Section 3: Použité datasety ───────────────────────────────────────────────

DATASETS = [
    "Hranice městských částí (IPR Praha)",
    "Objekty Městské policie (Geoportál Praha)",
    "Parkovací automaty (Geoportál Praha)",
    "Stání ZTP (Geoportál Praha)",
    "P+R parkoviště (Geoportál Praha)",
    "Placené stání (Geoportál Praha)",
    "Zákazy stání (Geoportál Praha)",
    "Vstupy do metra (Geoportál Praha)",
    "Parky a zeleň (OpenStreetMap / Overpass API)",
    "Nextbike stanice (GBFS v2.3)",
    "Zastávky PID (Ropid open data)",
    "Stanice kvality ovzduší (ČHMÚ)",
    "Demografické údaje MČ (ČSÚ, 2004–2025)",
]

datasets = _section_card(
    "fa-database", "Použité datasety", "#0f766e",
    [
        html.P(
            "Všechna data jsou veřejně dostupná a pravidelně aktualizovaná. "
            "Podrobná dokumentace každého zdroje je k dispozici na stránce Datové sady.",
            style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1rem",
                   "lineHeight": "1.6"}
        ),
        html.Div(
            [_dataset_chip(ds) for ds in DATASETS],
            style={"display": "flex", "flexWrap": "wrap", "gap": "0"}
        ),
        html.Div([
            html.I(className="fa-solid fa-circle-info",
                   style={"color": "#0f766e", "marginRight": "0.5rem", "fontSize": "0.9rem"}),
            html.Span(
                "Prostorová analýza je prováděna na úrovni 57 pražských městských částí. "
                "Hustoty jsou přepočítány na km² plochy obvodu.",
                style={"fontSize": "0.85rem", "color": "#475569"}
            )
        ], className="d-flex align-items-start mt-3",
           style={"background": "#f0fdf4", "padding": "0.75rem 1rem",
                  "borderRadius": "0.75rem", "border": "1px solid #bbf7d0"})
    ]
)


# ── Section 4: Jak navigovat aplikací ────────────────────────────────────────

navigation = _section_card(
    "fa-compass", "Jak navigovat aplikací", "#d97706",
    [
        html.P(
            "Aplikace je strukturována tak, aby umožnila jak rychlý přehled, tak hlubokou "
            "analýzu. Níže najdete stručný průvodce každou sekcí.",
            style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1.25rem",
                   "lineHeight": "1.6"}
        ),
        _nav_row("fa-house-door", "Domů",
                 "vstupní bod s přehledem funkcí a kontextem aplikace",
                 "#667eea"),
        _nav_row("fa-geo-alt", "Městské části",
                 "interaktivní mapa; kliknutím na obvod přejdete na detail",
                 "#0ea5e9"),
        _nav_row("fa-map-pin", "Detail obvodu",
                 "bezpečnost, doprava, přístupnost, mobilita, prostředí a demografické údaje; "
                 "kliknutím na kartu zobrazíte příslušnou vrstvu na mapě",
                 "#10b981"),
        _nav_row("fa-bar-chart", "Dashboard",
                 "porovnání obvodů; výběr datasetu a obvodu; přepínač raw počet / hustota na km²",
                 "#f59e0b"),
        _nav_row("fa-graph-up", "QoL Index",
                 "kompozitní skóre 4 QOUL domén; radarový diagram a žebříček obvodů",
                 "#8b5cf6"),
        _nav_row("fa-book", "Teorie",
                 "vysvětlení teoretického rámce za dashboardem (WHOQOL, QOUL, 15-min city, SSF)",
                 "#764ba2"),
        _nav_row("fa-people-group", "Persony",
                 "pohled na data očima tří reprezentativních uživatelů: Jan, Elena, Novákovi",
                 "#be185d"),
        _nav_row("fa-database", "Datové sady",
                 "dokumentace všech datových zdrojů — původ, formát, frekvence aktualizace",
                 "#0f766e"),
    ]
)


# ── Layout ────────────────────────────────────────────────────────────────────

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            page_title("O Aplikaci", align="center", use_gradient=True),
            intro,
            theory,
            datasets,
            navigation,
        ], width=12)
    ])
], fluid=True, className="py-2")
