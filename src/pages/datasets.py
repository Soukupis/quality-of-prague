"""Datasets documentation page.

This page displays documentation for all available datasets in the application.
Shows README files from the data directory in a single expandable accordion,
providing descriptions and metadata for each dataset.
"""
import dash_bootstrap_components as dbc
from dash import html, dcc, register_page
from src.components.ui import page_title
from src.utils.readme_utils import get_data_readmes

register_page(__name__, path="/datasets", name="Datové sady")

readmes = [r for r in get_data_readmes() if r["title"] != "Project Data Directory"]


def _icon_for_title(title: str):
    """Return (fa_icon_class, color) based on keyword matching of dataset title."""
    t = title.lower()
    if "policie" in t or "police" in t:
        return "fa-shield-halved", "#0f766e"
    if "parkovaci" in t or "parking" in t:
        return "fa-parking", "#1d4ed8"
    if "metro" in t or "vstupy" in t:
        return "fa-train-subway", "#7c3aed"
    if "park" in t or "zelen" in t:
        return "fa-tree", "#16a34a"
    if "nextbike" in t or "kolo" in t:
        return "fa-bicycle", "#0891b2"
    if "zastavky" in t or "pid" in t or "doprava" in t:
        return "fa-bus", "#7c3aed"
    if "ovzdusi" in t or "chmi" in t:
        return "fa-wind", "#14532d"
    if "demograf" in t or "csu" in t:
        return "fa-people-group", "#92400e"
    return "fa-database", "#64748b"


accordion_items = []
for i, readme in enumerate(readmes):
    icon, color = _icon_for_title(readme["title"])
    title_div = html.Div([
        html.I(className=f"fa-solid {icon} me-2", style={"color": color}),
        html.Span(readme["title"], style={"fontWeight": "600"})
    ])
    accordion_items.append(
        dbc.AccordionItem(
            dcc.Markdown(
                readme["markdown"],
                className="about-markdown compact-markdown",
            ),
            title=title_div,
            item_id=f"dataset-{i}",
        )
    )

accordion = dbc.Accordion(
    accordion_items,
    always_open=True,
    start_collapsed=True,
)

accordion_card = dbc.Card([
    dbc.CardBody([accordion])
], className="shadow-sm", style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"})

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            page_title(
                "Datové sady",
                align="center",
                description="Procházejte datasety, které stojí za analýzami a vizualizacemi.",
                use_gradient=True
            ),
            dbc.Row([
                dbc.Col([
                    html.P([
                        "Tato stránka přehledně zobrazuje datové zdroje využívané dashboardem. ",
                        "Celkem je k dispozici ",
                        dbc.Badge(
                            f"{len(readmes)} datasetů",
                            color="primary",
                            className="ms-1 me-1",
                            pill=True,
                        ),
                        " — rozbalte libovolnou položku pro podrobný popis.",
                    ], className="text-muted mb-3", style={"fontSize": "0.97rem"}),
                ], width=12)
            ]),
            accordion_card,
        ], width=12)
    ])
], fluid=True, className="py-2")
