import dash_bootstrap_components as dbc
from dash import html, register_page
from components.ui import page_title, page_subtitle, page_divider, feature_card

register_page(__name__, path="/", name="Home")

feature_cards = dbc.Row([
    dbc.Col([
        feature_card(
            icon_name="bar-chart",
            title="Dashboard",
            description="Interactive insights and metrics about Prague's quality of life.",
            button_text="Go to Dashboard",
            button_href="/dashboard"
        )
    ], md=3, xs=12, className="mb-4"),
    dbc.Col([
        feature_card(
            icon_name="geo-alt",
            title="Districts",
            description="Explore quality of life metrics across Prague's districts.",
            button_text="View Districts",
            button_href="/districts"
        )
    ], md=3, xs=12, className="mb-4"),
    dbc.Col([
        feature_card(
            icon_name="database",
            title="Datasets",
            description="Browse the datasets powering the analysis and visualizations.",
            button_text="View Datasets",
            button_href="/datasets"
        )
    ], md=3, xs=12, className="mb-4"),
    dbc.Col([
        feature_card(
            icon_name="info-circle",
            title="About",
            description="Learn more about the purpose and background of this platform.",
            button_text="About",
            button_href="/about"
        )
    ], md=3, xs=12, className="mb-4"),
], className="g-4 justify-content-center")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            page_title("Quality of Prague"),
            page_subtitle("A platform for analyzing and presenting quality of life metrics for Prague."),
            page_divider(),
            html.P(
                "Explore the dashboard for insights, learn more about the project, view districts, or browse the datasets.",
                className="mb-4",
                style={"fontSize": "1.05rem"}
            ),
            feature_cards
        ], width=12)
    ])
], fluid=True, className="py-2")
