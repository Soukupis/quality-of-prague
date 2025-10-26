import dash_bootstrap_components as dbc
from dash import html, register_page

register_page(__name__, path="/", name="Home")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Welcome to Quality of Prague", className="display-4 mb-4"),
            html.P(
                "Discover and explore the quality of life metrics across Prague. "
                "This platform provides comprehensive insights into various aspects "
                "that make Prague a great place to live, work, and visit.",
                className="lead mb-4"
            ),
            html.Hr(className="my-4"),
            html.P(
                "Navigate through our dashboard to see detailed analytics and "
                "learn more about what makes Prague special.",
                className="mb-4"
            ),
            dbc.Button(
                "View Dashboard",
                color="primary",
                href="/dashboard",
                size="lg",
                className="me-3"
            ),
            dbc.Button(
                "Learn More",
                color="outline-secondary",
                href="/about",
                size="lg"
            )
        ], width=12)
    ], className="justify-content-center text-center")
], fluid=True, className="py-5")
