import dash_bootstrap_components as dbc
from dash import html, register_page
from src.components.ui import feature_card, page_title

register_page(__name__, path="/", name="Domů")

storytelling_section = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(
                    "Porovnejte data",
                    className="text-center mb-3",
                    style={
                        "fontWeight": "700",
                        "fontSize": "2rem",
                        "color": "#667eea",
                        "letterSpacing": "-0.5px",
                        "lineHeight": "1.2"
                    }
                ),
                html.P(
                    "Analyzujte a porovnávejte data napříč městskými částmi",
                    className="text-center mb-4",
                    style={
                        "fontSize": "1rem",
                        "color": "#6c757d",
                        "lineHeight": "1.5",
                        "fontWeight": "400"
                    }
                ),
                html.A([
                    dbc.Card([
                        dbc.CardBody([
                            html.Img(
                                src="/assets/analytics_image.png",
                                className="img-fluid",
                                alt="Dashboard Analytics",
                                style={
                                    "width": "100%",
                                    "height": "450px",
                                    "objectFit": "contain",
                                    "padding": "2rem"
                                }
                            )
                        ], className="p-0")
                    ], className="story-card shadow-sm", style={
                        "border": "none",
                        "borderRadius": "1rem",
                        "overflow": "hidden",
                        "transition": "all 0.3s ease",
                        "background": "linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%)"
                    })
                ], href="/dashboard", style={"textDecoration": "none"}),
            ], style={"padding": "1.5rem"})
        ], md=6, xs=12, className="mb-4"),
        dbc.Col([
            html.Div([
                html.H2(
                    "Prozkoumejte městské části",
                    className="text-center mb-3",
                    style={
                        "fontWeight": "700",
                        "fontSize": "2rem",
                        "color": "#764ba2",
                        "letterSpacing": "-0.5px",
                        "lineHeight": "1.2"
                    }
                ),
                html.P(
                    "Detailní přehled každé městské části a jejích charakteristik",
                    className="text-center mb-4",
                    style={
                        "fontSize": "1rem",
                        "color": "#6c757d",
                        "lineHeight": "1.5",
                        "fontWeight": "400"
                    }
                ),
                html.A([
                    dbc.Card([
                        dbc.CardBody([
                            html.Img(
                                src="/assets/bar_chart_image.png",
                                className="img-fluid",
                                alt="City Districts",
                                style={
                                    "width": "100%",
                                    "height": "450px",
                                    "objectFit": "contain",
                                    "padding": "2rem"
                                }
                            )
                        ], className="p-0")
                    ], className="story-card shadow-sm", style={
                        "border": "none",
                        "borderRadius": "1rem",
                        "overflow": "hidden",
                        "transition": "all 0.3s ease",
                        "background": "#ffffff"
                    })
                ], href="/districts", style={"textDecoration": "none"}),
            ], style={"padding": "1.5rem"})
        ], md=6, xs=12, className="mb-4"),
    ], className="g-4")
], style={"marginBottom": "4rem", "marginTop": "2rem"})

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            page_title(
                "Quality of Prague",
                align="center",
                description="Objevte kvalitu života v Praze skrz data a interaktivní vizualizace",
                use_gradient=True
            ),
            storytelling_section,
        ], width=12)
    ])
], fluid=True, className="py-2")
