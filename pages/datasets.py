import dash_bootstrap_components as dbc
from dash import html, dcc, register_page
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
            always_open=False,
            id="accordion-{}".format(i),
            className="mb-3"
        )
    )

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            [
                html.H1("Datasets Documentation", className="display-5 mb-4", style={"fontWeight": 700, "fontSize": "2.2rem"}),
                html.P(
                    "Below you will find documentation for all datasets used in this project. "
                    "Each section provides details, structure, and source information.",
                    className="lead mb-4", style={"fontSize": "1.08rem"}
                ),
                html.Hr(className="mb-4"),
            ] + readme_dropdowns,
            width=10, className="mx-auto"
        )
    ], className="justify-content-center mb-5"),
], fluid=True, className="py-2")
