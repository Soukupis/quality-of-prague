"""Dash callbacks for district map interactions and layer toggling.

This module handles all callback logic for the district detail map, including:
- Redirecting to district pages from map clicks
- Toggling map layer visibility
- Restoring layer states from session storage
- Managing UI states for layer control cards

All callbacks use pattern-matching IDs for dynamic layer management.
"""
from dash import Input, Output, callback, State, ctx, exceptions, ALL
from src.components.graphs import create_single_district_map
from src.configs.data_config import DATA_PATHS
from src.utils.loaders.data_loader import read_file
from src.utils.polygons.polygon_utils import build_polygon_config
from src.utils.scatter.scatter_utils import build_scatter_config
from src.configs.dataset_config import DATASET_CONFIGS

def get_prague_districts_lookup():
    """Load Prague districts and create ID-to-name lookup table.

    Reads the Prague districts GeoJSON file, converts it to WGS84 coordinate
    system, and creates a simple lookup table mapping district IDs (indices)
    to district names.

    Returns:
        pd.DataFrame: DataFrame with 'id' (int) and 'name' (str) columns for
            district lookup. Unknown districts are labeled as "Unknown".

    Examples:
        >>> lookup = get_prague_districts_lookup()
        >>> print(lookup.head())
           id         name
        0   0     Praha 1
        1   1     Praha 2
    """
    df = read_file(DATA_PATHS.prague_districts)
    df = df.to_crs(4326)
    df["id"] = df.index
    df["name"] = df["nazev_1"].fillna("Unknown")
    return df[["id", "name"]]


@callback(
    Output("url", "href"),
    Input("prague-map", "clickData"),
)
def redirect_to_selected_district(click_data):
    """Redirect user to district detail page when clicking a district on the map.

    Dash callback that processes map click events and navigates to the district
    detail page for the clicked district. Validates that the click corresponds
    to a valid district before redirecting.

    Args:
        click_data: Dictionary containing click event data from Plotly map.
            Expected structure: {'points': [{'location': <district_id>, ...}]}

    Returns:
        str: URL path to the district detail page with district name query
            parameter (e.g., "/districts/district-detail?district=Praha 1").

    Raises:
        exceptions.PreventUpdate: If click_data is None, doesn't contain valid
            point data, or the district ID doesn't match any known district.

    Examples:
        This is a Dash callback triggered automatically:
        >>> # User clicks on Praha 1 district on map
        >>> # Callback executes: redirect_to_selected_district({...})
        >>> # Returns: "/districts/district-detail?district=Praha 1"
        >>> # Browser navigates to that URL
    """
    if click_data and click_data.get("points"):
        location_id = click_data["points"][0]["location"]
        district_lookup = get_prague_districts_lookup()
        district_row = district_lookup[district_lookup["id"] == location_id]
        if not district_row.empty:
            district_name = district_row["name"].iloc[0]
            return "/districts/district-detail" + f"?district={district_name}"
        else:
            raise exceptions.PreventUpdate
    raise exceptions.PreventUpdate


@callback(
    [Output('single-district-map', 'figure', allow_duplicate=True),
     Output({'type': 'layer-plus-icon', 'index': ALL}, 'style', allow_duplicate=True),
     Output({'type': 'layer-minus-icon', 'index': ALL}, 'style', allow_duplicate=True),
     Output({'type': 'layer-card', 'index': ALL}, 'className', allow_duplicate=True)],
    Input('visible-layers-store', 'data'),
    State('district-store', 'data'),
    prevent_initial_call='initial_duplicate'
)
def restore_map_state(visible_layers, district):
    """Restore map layers and UI state from session storage on page load.

    This callback runs when the district detail page loads and reads the
    previously selected layer visibility state from session storage. It
    recreates the map with the correct layers visible and restores the
    UI state of layer control cards (icons and styling).

    Args:
        visible_layers: List of layer keys (strings) that were visible when
            the user last viewed this page. Read from dcc.Store. Can be None
            or empty list.
        district: Name of the current district (e.g., "Praha 1"). Read from
            dcc.Store.

    Returns:
        tuple: Contains 4 elements:
            - go.Figure: Plotly map figure with restored layer visibility
            - list[dict]: Styles for plus icons (display: block/none)
            - list[dict]: Styles for minus icons (display: block/none)
            - list[str]: CSS class names for cards ("info-card-selected" or "")

    Examples:
        This callback is triggered automatically on page load:
        >>> # User navigates to district page
        >>> # Session storage contains: ["parking_meters", "subway_entrances"]
        >>> # Callback restores map with those layers visible
        >>> # UI shows minus icons and selected styling for those cards
    """
    visible_layers = visible_layers or []

    if not district:
        figure = create_single_district_map(district, None)
    else:
        scatters = build_scatter_config(district, visible_layers)
        polygons = build_polygon_config(district, visible_layers)
        figure = create_single_district_map(district, scatters if scatters else None, polygons if polygons else None)

    plus_styles, minus_styles, card_classes = handle_card_styles(visible_layers)

    return figure, plus_styles, minus_styles, card_classes


@callback(
    [Output('single-district-map', 'figure'),
     Output('visible-layers-store', 'data'),
     Output({'type': 'layer-plus-icon', 'index': ALL}, 'style'),
     Output({'type': 'layer-minus-icon', 'index': ALL}, 'style'),
     Output({'type': 'layer-card', 'index': ALL}, 'className')],
    Input({'type': 'layer-card', 'index': ALL}, 'n_clicks'),
    [State('visible-layers-store', 'data'),
     State('district-store', 'data')],
    prevent_initial_call=True
)
def toggle_map_layer(n_clicks_list, visible_layers, district):
    """Toggle map layer visibility when user clicks layer control cards.

    This callback responds to clicks on layer control cards (e.g., "Parking Meters",
    "Metro Entrances"). When clicked, it toggles the visibility of that layer on
    the map, updates the session storage, and updates the card UI to show the
    new state (plus/minus icons and selected styling).

    Uses pattern-matching callbacks to handle multiple layer cards dynamically.

    Args:
        n_clicks_list: List of click counts for all layer cards. Used by Dash
            to detect which card was clicked.
        visible_layers: List of currently visible layer keys (strings) from
            session storage. Can be None or empty list.
        district: Name of the current district (e.g., "Praha 1").

    Returns:
        tuple: Contains 5 elements:
            - go.Figure: Updated Plotly map with toggled layer
            - list[str]: Updated list of visible layer keys for session storage
            - list[dict]: Styles for plus icons
            - list[dict]: Styles for minus icons
            - list[str]: CSS class names for cards

    Raises:
        exceptions.PreventUpdate: If no card was clicked or if the clicked
            card doesn't match any known dataset configuration.

    Examples:
        This callback triggers when user clicks a layer card:
        >>> # User clicks "Parking Meters" card
        >>> # visible_layers = []
        >>> # After callback: visible_layers = ["parking_meters"]
        >>> # Map updates to show parking meter points
        >>> # Card shows minus icon and selected styling
    """
    visible_layers = visible_layers or []

    # Find which card was clicked
    triggered = ctx.triggered_id
    if not triggered:
        raise exceptions.PreventUpdate

    # Get the dataset key from the triggered card
    clicked_index = triggered['index']

    # Find the corresponding layer key
    clicked_config = DATASET_CONFIGS.get(clicked_index)
    if not clicked_config:
        raise exceptions.PreventUpdate

    layer_key = clicked_config["layer_key"]

    if layer_key in visible_layers:
        visible_layers.remove(layer_key)
    else:
        visible_layers.append(layer_key)

    # Build scatter configuration and update map
    scatters = build_scatter_config(district, visible_layers)
    polygons = build_polygon_config(district, visible_layers)
    updated_figure = create_single_district_map(district, scatters if scatters else None, polygons if polygons else None)

    plus_styles, minus_styles, card_classes = handle_card_styles(visible_layers)

    return updated_figure, visible_layers, plus_styles, minus_styles, card_classes

def handle_card_styles(visible_layers):
    """Generate icon styles and CSS classes for layer control cards.

    Creates the appropriate CSS styles and class names for layer control cards
    based on which layers are currently visible. Shows minus icons for visible
    layers and plus icons for hidden layers.

    Args:
        visible_layers: List of layer keys (strings) that are currently visible
            on the map. Can be empty list.

    Returns:
        tuple: Contains 3 lists, one for each dataset in DATASET_CONFIGS:
            - list[dict]: Plus icon styles ({'display': 'block'} or {'display': 'none'})
            - list[dict]: Minus icon styles ({'display': 'block'} or {'display': 'none'})
            - list[str]: Card CSS classes ("info-card-selected" or "")

    Examples:
        >>> styles = handle_card_styles(["parking_meters"])
        >>> # For parking_meters card:
        >>> # plus_styles[0] = {'display': 'none'}
        >>> # minus_styles[0] = {'display': 'block'}
        >>> # card_classes[0] = "info-card-selected"
        >>> # For other cards: opposite values
    """
    plus_styles = []
    minus_styles = []
    card_classes = []

    for dataset_key, config in DATASET_CONFIGS.items():
        # Only produce values for datasets that render info_card layer toggles
        # (section="safety" or "travel"). Other sections don't put layer-plus/minus
        # icons in the DOM, so including them would cause an ALL pattern count mismatch.
        if config.get("section") not in ("safety", "travel"):
            continue
        layer_key = config["layer_key"]
        is_visible = layer_key in visible_layers

        plus_styles.append({"display": "none"} if is_visible else {"display": "block"})
        minus_styles.append({"display": "block"} if is_visible else {"display": "none"})
        card_classes.append("info-card-selected" if is_visible else "")
    return plus_styles, minus_styles, card_classes
