import dash_bootstrap_components as dbc
from dash import html, dcc, register_page
from utils.readme_utils import get_data_readmes, build_readme_cards

register_page(__name__, path="/about", name="About")

# Only show the main data directory README on the About page for brevity
all_readmes = get_data_readmes()
main_readme = [r for r in all_readmes if r["title"] == "Project Data Directory"]
readme_cards = build_readme_cards(main_readme, compact=True)

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            [
                html.H1("About Quality of Prague", className="display-6 mb-3", style={"fontSize": "2rem"}),
                html.P(
                    "Quality of Prague is a platform for analyzing and presenting quality of life metrics for Prague.",
                    className="lead mb-3", style={"fontSize": "1.1rem"}
                ),
                html.Hr(className="mb-3"),
                html.H2("Project Data Directory", className="mt-3 mb-2", style={"fontSize": "1.1rem"}),
            ] + readme_cards,
            width=9, className="mx-auto"
        )
    ], className="justify-content-center mb-4"),
], fluid=True, className="py-1")
