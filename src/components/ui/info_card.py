from dash import html
import dash_bootstrap_components as dbc

def info_card(icon=None, title="", value="", variant=None, card_id=None, dataset_key=None, compact=False, color="#334155"):
    """Create an interactive information card component.

    Builds a Bootstrap card displaying an icon, title, and value. Can be made
    clickable with toggle icons (plus/minus) for interactive layer control.
    Supports pattern-matching IDs for dynamic callbacks.

    Args:
        icon: Font Awesome icon class (e.g., "fa-map-marker"). Optional.
        title: Card title text to display.
        value: Value or metric to display (can be string or number).
        variant: Style variant for the card (adds `info-card-{variant}` class).
            Optional.
        card_id: ID for the card wrapper, makes card clickable. If provided,
            adds toggle icons. Optional.
        dataset_key: Key for pattern-matching callbacks. Creates dict-based IDs
            instead of string IDs. Optional.
        compact: When True, renders a compact card layout with icon on the left,
            label above value in the centre, and a small toggle icon on the right.
            The fixed min/max-width CSS constraints are removed so the card fills
            its grid column. Defaults to False (original layout unchanged).

    Returns:
        Dash component: dbc.Card wrapped in html.Div if card_id provided,
            otherwise just dbc.Card.

    Examples:
        >>> # Simple info card
        >>> card = info_card(
        ...     icon="fa-building",
        ...     title="Districts",
        ...     value="22"
        ... )
        >>>
        >>> # Interactive card with pattern-matching ID
        >>> card = info_card(
        ...     icon="fa-parking",
        ...     title="Parking Meters",
        ...     value="1,234",
        ...     card_id="parking-card",
        ...     dataset_key="parking_meters"
        ... )
        >>>
        >>> # Compact interactive card
        >>> card = info_card(
        ...     icon="fa-shield-halved",
        ...     title="Police",
        ...     value="3",
        ...     card_id="police-card",
        ...     dataset_key="police_stations",
        ...     compact=True
        ... )
    """
    base_class = "info-card"
    variant_class = f"info-card-{variant}" if variant else ""
    card_class = f"{base_class} {variant_class}".strip()

    if card_id:
        card_class += " info-card-clickable"

    # Use pattern-matching IDs if dataset_key is provided, otherwise use simple string IDs
    if dataset_key:
        plus_icon_id = {'type': 'layer-plus-icon', 'index': dataset_key}
        minus_icon_id = {'type': 'layer-minus-icon', 'index': dataset_key}
    else:
        plus_icon_id = f"{card_id}-plus-icon" if card_id else None
        minus_icon_id = f"{card_id}-minus-icon" if card_id else None

    if compact:
        card = dbc.Card(
            dbc.CardBody(
                html.Div([
                    html.I(
                        className=f"fa-solid {icon}",
                        style={"fontSize": "1.3rem", "color": color,
                               "minWidth": "1.6rem", "flexShrink": "0"}
                    ) if icon else None,
                    html.Div([
                        html.Div(title, style={"fontSize": "0.8rem", "color": "#64748b",
                                               "fontWeight": "500", "lineHeight": "1.2"}),
                        html.Div(str(value), style={"fontSize": "1.3rem", "fontWeight": "700",
                                                    "color": "#1e293b", "lineHeight": "1.3"}),
                    ], style={"marginLeft": "0.5rem", "flexGrow": "1", "minWidth": "0"}),
                    html.Div([
                        html.I(
                            id=plus_icon_id,
                            className="fa-solid fa-circle-plus",
                            style={"display": "block", "fontSize": "1rem", "color": "#94a3b8"}
                            if card_id else {"display": "none"}
                        ),
                        html.I(
                            id=minus_icon_id,
                            className="fa-solid fa-circle-minus",
                            style={"display": "none", "fontSize": "1rem", "color": "#4A90E2"}
                        ),
                    ]) if card_id else None,
                ], className="d-flex align-items-center")
            ),
            className="shadow-sm h-100",
            style={"border": "none", "borderRadius": "0.75rem",
                   "background": "linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%)"},
        )
    else:
        card = dbc.Card(
            dbc.CardBody(
                html.Div([
                    html.Div([
                        html.I(
                            id=plus_icon_id,
                            className="fa-solid fa-square-plus info-card-toggle-icon",
                            style={"display": "block"} if card_id else {"display": "none"}
                        ),
                        html.I(
                            id=minus_icon_id,
                            className="fa-solid fa-square-minus info-card-toggle-icon",
                            style={"display": "none"}
                        )
                    ]) if card_id else None,
                    html.Div(className="info-card-divider") if card_id else None,
                    html.I(className=f"fa-solid {icon} info-card-icon") if icon else None,
                    html.Div([
                        html.H4(title, className="info-card-title mb-0"),
                        html.Span(value, className="info-card-number")
                    ], className="d-flex flex-column flex-sm-row align-items-start align-items-sm-center gap-1 flex-grow-1")
                ], className="d-flex align-items-center justify-content-start gap-2 w-100")
            ),
            className=card_class,
        )

    if card_id:
        wrapper_id = {'type': 'layer-card', 'index': dataset_key} if dataset_key else card_id

        return html.Div(
            card,
            id=wrapper_id,
            n_clicks=0,
            style={"cursor": "pointer", "height": "100%"}
        )

    return card

