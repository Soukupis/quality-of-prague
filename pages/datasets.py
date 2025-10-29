import dash_bootstrap_components as dbc
from dash import html, dcc, register_page
from components.ui.page_heading import page_title, page_subtitle, page_divider
from utils.readme_utils import get_data_readmes

register_page(__name__, path="/datasets", name="Datasets")

readmes = [r for r in get_data_readmes() if r["title"] != "Project Data Directory"]

readme_dropdowns = []
for i, readme in enumerate(readmes):
    readme_dropdowns.append(
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    dbc.CardBody([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.H5(readme["title"], className="mb-2", style={"fontWeight": 600, "fontSize": "1.1rem"}),
                                        dbc.Card(
                                            dbc.CardBody([
                                                dcc.Markdown(
                                                    readme["markdown"],
                                                    className="about-markdown compact-markdown",
                                                    style={
                                                        "background": "#f8f9fa",
                                                        "padding": "0.75rem 1rem",
                                                        "borderRadius": "0.4rem",
                                                        "textAlign": "left",
                                                        "fontSize": "0.97rem",
                                                        "overflowX": "auto",
                                                        "lineHeight": "1.5",
                                                        "margin": 0
                                                    }
                                                )
                                            ]),
                                            className="mb-0 shadow-none",
                                            style={"border": "none", "boxShadow": "none", "background": "none"}
                                        )
                                    ])
                                ])
                            ])
                        ], className="mb-0 shadow-none", style={"border": "none", "boxShadow": "none", "background": "none"})
                    ]),
                    title=readme["title"],
                    item_id="dataset-{}".format(i)
                )
            ],
            start_collapsed=True,
            flush=True,
            className="mb-2"
        )
    )

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            page_title("Datasets", icon_name="database"),
            page_subtitle("Browse the datasets powering the analysis and visualizations."),
            page_divider(),
            *readme_dropdowns
        ], width=12)
    ])
], fluid=True, className="py-2")
