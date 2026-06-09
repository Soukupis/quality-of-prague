"""Datasets documentation page."""
import dash_bootstrap_components as dbc
from dash import html, dcc, register_page
from src.components.ui import page_title
from src.utils.readme_utils import get_data_readmes
from src.i18n import t

register_page(__name__, path="/datasets", name="Datové sady")

readmes = [r for r in get_data_readmes() if r["title"] != "Project Data Directory"]


def _icon_for_title(title: str):
    tl = title.lower()
    if "policie" in tl or "police" in tl:
        return "fa-shield-halved", "#0f766e"
    if "parkovaci" in tl or "parking" in tl:
        return "fa-parking", "#1d4ed8"
    if "metro" in tl or "vstupy" in tl:
        return "fa-train-subway", "#7c3aed"
    if "park" in tl or "zelen" in tl:
        return "fa-tree", "#16a34a"
    if "nextbike" in tl or "kolo" in tl:
        return "fa-bicycle", "#0891b2"
    if "zastavky" in tl or "pid" in tl or "doprava" in tl:
        return "fa-bus", "#7c3aed"
    if "ovzdusi" in tl or "chmi" in tl:
        return "fa-wind", "#14532d"
    if "demograf" in tl or "csu" in tl:
        return "fa-people-group", "#92400e"
    return "fa-database", "#64748b"


def _build_accordion():
    items = []
    for i, readme in enumerate(readmes):
        icon_class, color = _icon_for_title(readme["title"])
        title_div = html.Div([
            html.I(className=f"fa-solid {icon_class} me-2", style={"color": color}),
            html.Span(readme["title"], style={"fontWeight": "600"}),
        ])
        items.append(dbc.AccordionItem(
            dcc.Markdown(readme["markdown"], className="about-markdown compact-markdown"),
            title=title_div,
            item_id=f"dataset-{i}",
        ))
    return items


def layout(lang="cs"):
    accordion_items = _build_accordion()
    accordion = dbc.Accordion(accordion_items, always_open=True, start_collapsed=True)
    accordion_card = dbc.Card(
        dbc.CardBody([accordion]),
        className="shadow-sm",
        style={"border": "1px solid #e2e8f0", "borderRadius": "1rem"},
    )

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                page_title(
                    t("datasets_title", lang),
                    align="center",
                    description=t("datasets_desc", lang),
                    use_gradient=True,
                ),
                dbc.Row([dbc.Col([
                    html.P([
                        t("datasets_available_prefix", lang),
                        dbc.Badge(
                            t("datasets_available_badge", lang, n=len(readmes)),
                            color="primary", className="ms-1 me-1", pill=True,
                        ),
                        t("datasets_available_suffix", lang),
                    ], className="text-muted mb-3", style={"fontSize": "0.97rem"}),
                ], width=12)]),
                accordion_card,
            ], width=12)
        ])
    ], fluid=True, className="py-2")
