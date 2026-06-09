"""Quality of Life theoretical framework page.

Explains the theoretical foundation behind the dashboard, drawn directly
from the master thesis. Covers WHOQOL, QOUL 4-domain framework, the
15-Minute City concept, and the central objective vs. subjective distinction.

Czech language is used throughout to match the application's language.
"""
import dash_bootstrap_components as dbc
from dash import register_page, html
from src.components.ui import page_title

register_page(__name__, path="/theory", name="Teorie")


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


def _domain_badge(label, color, text_color="white"):
    return html.Span(
        label,
        style={
            "display": "inline-block",
            "background": color,
            "color": text_color,
            "borderRadius": "12px",
            "padding": "4px 14px",
            "fontSize": "0.82rem",
            "fontWeight": "600",
            "marginRight": "0.4rem",
            "marginBottom": "0.4rem",
        }
    )


def _indicator_row(icon_class, label, description, color="#475569"):
    return html.Div([
        html.I(className=f"fa-solid {icon_class}",
               style={"fontSize": "1rem", "color": color, "minWidth": "1.5rem", "marginTop": "2px"}),
        html.Div([
            html.Span(label, style={"fontWeight": "600", "fontSize": "0.9rem", "color": "#1e293b"}),
            html.Span(f" — {description}", style={"fontSize": "0.88rem", "color": "#64748b"}),
        ], style={"marginLeft": "0.5rem"})
    ], className="d-flex align-items-start mb-2")


# ── Objective vs. Subjective ──────────────────────────────────────────────────
obj_vs_subj = _section_card(
    "fa-scale-balanced", "Objektivní vs. Subjektivní kvalita života", "#667eea",
    [
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className="fa-solid fa-ruler-combined",
                           style={"fontSize": "2rem", "color": "#3b82f6", "marginBottom": "0.5rem"}),
                    html.H6("Objektivní ukazatele", style={"fontWeight": "700", "color": "#1e293b"}),
                    html.P(
                        "Měřitelné fyzické charakteristiky — hustota zástavby, infrastruktura, "
                        "úroveň znečištění, dostupnost služeb. Tato data lze přímo sbírat a "
                        "vizualizovat z otevřených zdrojů jako Geoportál Praha nebo Golemio.",
                        style={"fontSize": "0.88rem", "color": "#475569", "lineHeight": "1.5"}
                    ),
                    html.Div([
                        _domain_badge("Vstupy do metra", "#dbeafe", "#1e3a8a"),
                        _domain_badge("Parkoviště ZTP", "#ede9fe", "#4c1d95"),
                        _domain_badge("Policejní stanice", "#dcfce7", "#14532d"),
                    ])
                ], style={"padding": "1rem", "background": "#f8faff",
                          "borderRadius": "0.75rem", "height": "100%"})
            ], md=6, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.I(className="fa-solid fa-heart-pulse",
                           style={"fontSize": "2rem", "color": "#a855f7", "marginBottom": "0.5rem"}),
                    html.H6("Subjektivní vnímání", style={"fontWeight": "700", "color": "#1e293b"}),
                    html.P(
                        "Individuální percepce, spokojenost a emoční stavy. Stejné objektivní "
                        "podmínky vedou k rozdílnému subjektivnímu prožitku — závisí na věku, "
                        "pohyblivosti, ekonomické situaci a osobních preferencích.",
                        style={"fontSize": "0.88rem", "color": "#475569", "lineHeight": "1.5"}
                    ),
                    html.Div([
                        _domain_badge("Spokojenost s bydlením", "#fae8ff", "#701a75"),
                        _domain_badge("Pocit bezpečí", "#fef3c7", "#78350f"),
                        _domain_badge("Subjektivní pohoda", "#ffe4e6", "#881337"),
                    ])
                ], style={"padding": "1rem", "background": "#fdf8ff",
                          "borderRadius": "0.75rem", "height": "100%"})
            ], md=6, className="mb-3"),
        ]),
        html.Div(
            html.P([
                html.I(className="fa-solid fa-quote-left",
                       style={"color": "#94a3b8", "marginRight": "0.5rem"}),
                "Samotné objektivní podmínky nestačí: vnímání a prožitek hrají klíčovou roli "
                "při určování pohody.",
                html.Span(" — Stiglitz-Sen-Fitoussi Commission (2009)", style={"color": "#94a3b8"})
            ], style={"fontSize": "0.88rem", "color": "#475569", "marginBottom": 0}),
            style={"background": "#f8fafc", "borderLeft": "4px solid #667eea",
                   "padding": "0.75rem 1rem", "borderRadius": "0 0.5rem 0.5rem 0"}
        )
    ]
)


# ── QOUL 4-domain framework ───────────────────────────────────────────────────
qoul_domains = _section_card(
    "fa-city", "QOUL — Čtyři domény kvality života v urbánním prostředí", "#0f766e",
    [
        html.P(
            "Operační rámec odvozený z indikátorové literatury. Tyto čtyři domény tvoří základ "
            "analytické struktury dashboardu.",
            style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1rem"}
        ),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("1", style={"background": "#0f766e", "color": "white",
                                              "borderRadius": "50%", "padding": "2px 8px",
                                              "fontWeight": "700", "marginRight": "0.5rem"}),
                        html.Span("Socioekonomická bezpečnost", style={"fontWeight": "700", "color": "#134e4a"}),
                    ], className="d-flex align-items-center mb-2"),
                    _indicator_row("fa-shield-halved", "Kriminalita", "policejní stanice / km²", "#0f766e"),
                    _indicator_row("fa-building-shield", "Infrastruktura bezpečnosti", "rozmístění v obvodu", "#0f766e"),
                ], style={"padding": "0.85rem", "background": "#f0fdfa",
                          "borderRadius": "0.75rem", "height": "100%"})
            ], md=6, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("2", style={"background": "#1d4ed8", "color": "white",
                                              "borderRadius": "50%", "padding": "2px 8px",
                                              "fontWeight": "700", "marginRight": "0.5rem"}),
                        html.Span("Mobilita", style={"fontWeight": "700", "color": "#1e3a8a"}),
                    ], className="d-flex align-items-center mb-2"),
                    _indicator_row("fa-train-subway", "Vstupy do metra", "počet a dostupnost", "#1d4ed8"),
                    _indicator_row("fa-elevator", "Bezbariérový přístup", "% vstupů s výtahem", "#1d4ed8"),
                    _indicator_row("fa-car-side", "Intermodalita (P+R)", "kapacita a plánování", "#1d4ed8"),
                ], style={"padding": "0.85rem", "background": "#eff6ff",
                          "borderRadius": "0.75rem", "height": "100%"})
            ], md=6, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("3", style={"background": "#7c3aed", "color": "white",
                                              "borderRadius": "50%", "padding": "2px 8px",
                                              "fontWeight": "700", "marginRight": "0.5rem"}),
                        html.Span("Přístupnost", style={"fontWeight": "700", "color": "#4c1d95"}),
                    ], className="d-flex align-items-center mb-2"),
                    _indicator_row("fa-wheelchair", "Parkoviště ZTP", "míst / km²", "#7c3aed"),
                    _indicator_row("fa-stairs", "Bezbariérové metro", "poměr vstupů s výtahem", "#7c3aed"),
                    _indicator_row("fa-map-pin", "Prostorová spravedlnost", "distribuce služeb", "#7c3aed"),
                ], style={"padding": "0.85rem", "background": "#faf5ff",
                          "borderRadius": "0.75rem", "height": "100%"})
            ], md=6, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("4", style={"background": "#b45309", "color": "white",
                                              "borderRadius": "50%", "padding": "2px 8px",
                                              "fontWeight": "700", "marginRight": "0.5rem"}),
                        html.Span("Zdraví prostředí", style={"fontWeight": "700", "color": "#78350f"}),
                    ], className="d-flex align-items-center mb-2"),
                    _indicator_row("fa-wind", "Kvalita ovzduší", "PM2.5, NO₂, O₃ (WHO 2021)", "#b45309"),
                    _indicator_row("fa-tree", "Zelené plochy", "dostupnost a vzdálenost", "#b45309"),
                    _indicator_row("fa-volume-high", "Hlukové znečištění", "dopravní zátěž", "#b45309"),
                ], style={"padding": "0.85rem", "background": "#fffbeb",
                          "borderRadius": "0.75rem", "height": "100%"})
            ], md=6, className="mb-3"),
        ])
    ]
)


# ── 15-Minute City ────────────────────────────────────────────────────────────
fifteen_min = _section_card(
    "fa-person-walking", "Město 15 minut (Moreno et al., 2021)", "#dc2626",
    [
        html.P(
            "Urbánní koncept, v němž jsou všechny klíčové funkce dostupné pěšky nebo na kole "
            "do 15 minut od domova. COVID-19 urychlil jeho přijetí — uzamčení odhalila "
            "zranitelnost oblastí závislých na automobilech.",
            style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1rem"}
        ),
        dbc.Row([
            dbc.Col([
                html.H6("6 klíčových sociálních funkcí", style={"fontWeight": "700",
                                                                   "color": "#7f1d1d", "marginBottom": "0.5rem"}),
                html.Div([
                    _domain_badge("Bydlení", "#fee2e2", "#7f1d1d"),
                    _domain_badge("Práce", "#fef3c7", "#78350f"),
                    _domain_badge("Nákupy", "#dcfce7", "#14532d"),
                    _domain_badge("Zdravotní péče", "#dbeafe", "#1e3a8a"),
                    _domain_badge("Vzdělání", "#ede9fe", "#4c1d95"),
                    _domain_badge("Volný čas", "#fce7f3", "#831843"),
                ], style={"marginBottom": "1rem"})
            ], md=6),
            dbc.Col([
                html.H6("4 dimenze realizace", style={"fontWeight": "700",
                                                        "color": "#7f1d1d", "marginBottom": "0.5rem"}),
                _indicator_row("fa-users", "Hustota", "optimální počet obyvatel / km²", "#dc2626"),
                _indicator_row("fa-location-dot", "Blízkost", "prostorová i časová dostupnost", "#dc2626"),
                _indicator_row("fa-shuffle", "Diverzita", "smíšené využití, sociální mix", "#dc2626"),
                _indicator_row("fa-wifi", "Digitalizace", "IoT, sdílená kola, big data", "#dc2626"),
            ], md=6),
        ]),
        html.Div(
            html.P([
                html.I(className="fa-solid fa-triangle-exclamation",
                       style={"color": "#f59e0b", "marginRight": "0.5rem"}),
                html.Strong("Důležité: "),
                "15 minut chůze pro mladého profesionála trvá ~25 minut pro seniora. "
                "Dimenze 'Blízkost' musí zohledňovat 'měkkou mobilitu' — přístupnost dle věku a pohyblivosti."
            ], style={"fontSize": "0.88rem", "color": "#475569", "marginBottom": 0}),
            style={"background": "#fffbeb", "borderLeft": "4px solid #f59e0b",
                   "padding": "0.75rem 1rem", "borderRadius": "0 0.5rem 0.5rem 0"}
        )
    ]
)


# ── WHOQOL ────────────────────────────────────────────────────────────────────
whoqol = _section_card(
    "fa-hospital", "WHOQOL — WHO Framework (6 domén)", "#0369a1",
    [
        html.P(
            "Mezinárodně validovaný nástroj pro měření kvality života na individuální úrovni. "
            "Vyvinut WHO ve 15 kulturně různorodých centrech. Klíčová vlastnost: "
            "\"WHOQOL staví myšlenky a pocity samotného člověka nad objektivní medicínské nálezy.\"",
            style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1rem"}
        ),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Span("Fyzická", style={"fontWeight": "700", "color": "#0369a1"}),
                    html.P("Energie, bolest, spánek, smyslové funkce",
                           style={"fontSize": "0.82rem", "color": "#64748b", "margin": 0})
                ], style={"padding": "0.6rem", "background": "#f0f9ff",
                          "borderRadius": "0.5rem", "marginBottom": "0.5rem"}),
                html.Div([
                    html.Span("Psychologická", style={"fontWeight": "700", "color": "#7c3aed"}),
                    html.P("Pozitivní pocity, sebehodnocení, negativní emoce",
                           style={"fontSize": "0.82rem", "color": "#64748b", "margin": 0})
                ], style={"padding": "0.6rem", "background": "#faf5ff",
                          "borderRadius": "0.5rem", "marginBottom": "0.5rem"}),
                html.Div([
                    html.Span("Úroveň nezávislosti", style={"fontWeight": "700", "color": "#0f766e"}),
                    html.P("Pohyblivost, denní aktivity, pracovní schopnost",
                           style={"fontSize": "0.82rem", "color": "#64748b", "margin": 0})
                ], style={"padding": "0.6rem", "background": "#f0fdfa",
                          "borderRadius": "0.5rem", "marginBottom": "0.5rem"}),
            ], md=6),
            dbc.Col([
                html.Div([
                    html.Span("Sociální vztahy", style={"fontWeight": "700", "color": "#be185d"}),
                    html.P("Osobní vztahy, sociální podpora, komunita",
                           style={"fontSize": "0.82rem", "color": "#64748b", "margin": 0})
                ], style={"padding": "0.6rem", "background": "#fdf2f8",
                          "borderRadius": "0.5rem", "marginBottom": "0.5rem"}),
                html.Div([
                    html.Span("Prostředí", style={"fontWeight": "700", "color": "#b45309"}),
                    html.P("Bezpečnost, bydlení, doprava, znečištění, rekreace, přístup ke zdravotní péči",
                           style={"fontSize": "0.82rem", "color": "#64748b", "margin": 0})
                ], style={"padding": "0.6rem", "background": "#fffbeb",
                          "borderRadius": "0.5rem", "marginBottom": "0.5rem"}),
                html.Div([
                    html.Span("Spiritualita / Víra", style={"fontWeight": "700", "color": "#6b7280"}),
                    html.P("Celkové vnímání kvality života a zdraví",
                           style={"fontSize": "0.82rem", "color": "#64748b", "margin": 0})
                ], style={"padding": "0.6rem", "background": "#f9fafb",
                          "borderRadius": "0.5rem", "marginBottom": "0.5rem"}),
            ], md=6),
        ])
    ]
)


# ── Personas ──────────────────────────────────────────────────────────────────
personas = _section_card(
    "fa-people-group", "Persony — různé potřeby ve stejném prostředí", "#7c3aed",
    [
        html.P(
            "Totéž objektivní prostředí vytváří rozdílný subjektivní prožitek podle věku, "
            "pohyblivosti a životního stylu. Přístup zdola-nahoru (bottom-up): zkušenosti "
            "z konkrétních domén tvoří celkovou spokojenost.",
            style={"fontSize": "0.9rem", "color": "#475569", "marginBottom": "1rem"}
        ),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fa-solid fa-person-cane",
                                   style={"fontSize": "1.8rem", "color": "#0f766e"}),
                            html.Div([
                                html.Div("Jan, 75 let", style={"fontWeight": "700", "color": "#134e4a"}),
                                html.Div("Holešovice, Praha 7", style={"fontSize": "0.8rem", "color": "#64748b"}),
                            ], style={"marginLeft": "0.5rem"})
                        ], className="d-flex align-items-center mb-2"),
                        html.Ul([
                            html.Li("Bezbariérové zastávky a metro", style={"fontSize": "0.82rem"}),
                            html.Li("Stromovka park — zelená plocha", style={"fontSize": "0.82rem"}),
                            html.Li("Efekt tepelného ostrova (dlažba)", style={"fontSize": "0.82rem"}),
                            html.Li("Parkoviště ZTP v blízkosti", style={"fontSize": "0.82rem"}),
                        ], style={"paddingLeft": "1rem", "marginBottom": 0})
                    ])
                ], style={"borderRadius": "0.75rem", "border": "1px solid #d1fae5",
                          "background": "#f0fdfa"})
            ], md=4, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fa-solid fa-person-biking",
                                   style={"fontSize": "1.8rem", "color": "#1d4ed8"}),
                            html.Div([
                                html.Div("Elena, 28 let", style={"fontWeight": "700", "color": "#1e3a8a"}),
                                html.Div("Karlín, Praha 8", style={"fontSize": "0.8rem", "color": "#64748b"}),
                            ], style={"marginLeft": "0.5rem"})
                        ], className="d-flex align-items-center mb-2"),
                        html.Ul([
                            html.Li("Metro + sdílené kolo (intermodalita)", style={"fontSize": "0.82rem"}),
                            html.Li("Pěší dostupnost smíšené zástavby", style={"fontSize": "0.82rem"}),
                            html.Li("Kvalita ovzduší a PM2.5", style={"fontSize": "0.82rem"}),
                            html.Li("Bezpečnost veřejných prostranství", style={"fontSize": "0.82rem"}),
                        ], style={"paddingLeft": "1rem", "marginBottom": 0})
                    ])
                ], style={"borderRadius": "0.75rem", "border": "1px solid #dbeafe",
                          "background": "#eff6ff"})
            ], md=4, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fa-solid fa-people-roof",
                                   style={"fontSize": "1.8rem", "color": "#b45309"}),
                            html.Div([
                                html.Div("Rodina Novákových", style={"fontWeight": "700", "color": "#78350f"}),
                                html.Div("Dejvice, Praha 6", style={"fontSize": "0.8rem", "color": "#64748b"}),
                            ], style={"marginLeft": "0.5rem"})
                        ], className="d-flex align-items-center mb-2"),
                        html.Ul([
                            html.Li("Školy a dětský lékař", style={"fontSize": "0.82rem"}),
                            html.Li("PM2.5 u Evropské ulice", style={"fontSize": "0.82rem"}),
                            html.Li("Bezpečné cyklostezky a hřiště", style={"fontSize": "0.82rem"}),
                            html.Li("Dostupnost zeleně pro děti", style={"fontSize": "0.82rem"}),
                        ], style={"paddingLeft": "1rem", "marginBottom": 0})
                    ])
                ], style={"borderRadius": "0.75rem", "border": "1px solid #fde68a",
                          "background": "#fffbeb"})
            ], md=4, className="mb-3"),
        ]),
    ]
)


# ── Measurement frameworks ────────────────────────────────────────────────────
measurement = _section_card(
    "fa-chart-line", "Metodologické přístupy k měření", "#6b7280",
    [
        dbc.Row([
            dbc.Col([
                html.H6("OECD Better Life Index", style={"fontWeight": "700", "color": "#1e293b",
                                                           "fontSize": "0.9rem"}),
                html.P("Kombinuje objektivní a subjektivní ukazatele. Uživatelsky nastavitelné "
                       "váhy domén. Sousedská (neighborhood) prostorová rozlišení.",
                       style={"fontSize": "0.82rem", "color": "#475569"}),
            ], md=4),
            dbc.Col([
                html.H6("WBCSD Mobilita", style={"fontWeight": "700", "color": "#1e293b",
                                                    "fontSize": "0.9rem"}),
                html.P("Klíčová metrika dojezdové doby: 10 min = nejlepší, 90 min = nejhorší. "
                       "Dostupnost MHD pro nejnižší příjmové skupiny.",
                       style={"fontSize": "0.82rem", "color": "#475569"}),
            ], md=4),
            dbc.Col([
                html.H6("Dienerova SWB", style={"fontWeight": "700", "color": "#1e293b",
                                                   "fontSize": "0.9rem"}),
                html.P("Frekvence pozitivních pocitů je lepším prediktorem pohody než intenzita "
                       "vzácných událostí. Malé, časté zlepšení prostředí > velké jednorázové projekty.",
                       style={"fontSize": "0.82rem", "color": "#475569"}),
            ], md=4),
        ])
    ]
)


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            page_title(
                "Teoretický rámec",
                align="center",
                description="Koncepty kvality života z akademické literatury, které stojí za analýzami v tomto dashboardu.",
                use_gradient=True
            ),
            obj_vs_subj,
            qoul_domains,
            fifteen_min,
            whoqol,
            personas,
            measurement,
        ], width=12)
    ])
], fluid=True, className="py-2")
