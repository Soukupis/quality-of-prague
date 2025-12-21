from dash import html
import dash_bootstrap_components as dbc

def info_card(icon=None, title="", value="", variant=None, card_id=None, dataset_key=None):
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
            style={"cursor": "pointer"}
        )

    return card

