from dash import Input, Output, callback, State, ctx, exceptions, ALL
from components.graphs import create_single_district_map
from data_config import DATA_PATHS
from utils.loaders.data_loader import read_file
from utils.scatter.scatter_utils import build_scatter_config
from dataset_config import DATASET_CONFIGS

def get_prague_districts_lookup():
    """
    Load Prague districts data and create a lookup table mapping district IDs to names.

    Returns:
        pd.DataFrame: DataFrame with columns 'id' (district index) and 'name' (district name)
    """
    df = read_file(str(DATA_PATHS.prague_districts))
    df = df.to_crs(4326)
    df["id"] = df.index
    df["name"] = df["nazev_1"].fillna("Unknown")
    return df[["id", "name"]]


@callback(
    Output("url", "href"),
    Input("prague-map", "clickData"),
)
def redirect_to_selected_district(click_data):
    """
    Redirects user the district info page after clicking on given district on map

    Args:
        click_data: point on the map the user has clicked on

    Returns:
        redirect: redirecting user to the given page if district exists, if not update is prevented
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
    """
    Restore map with previously selected layers when page loads.

    This callback runs when the page first loads and reads the visible_layers
    from session storage.
    If there are any layers saved, it recreates the map with those layers visible.
    Also restores the correct icon states.

    Args:
        visible_layers: List of layer keys from session storage
        district: Current district name

    Returns:
        tuple: (Figure with restored layer visibility, icon styles, card classes)
    """
    visible_layers = visible_layers or []

    if not district:
        figure = create_single_district_map(district, None)
    else:
        scatters = build_scatter_config(district, visible_layers)
        figure = create_single_district_map(district, scatters if scatters else None)

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
    """
    Toggle visibility of map layers when info cards are clicked.

    Args:
        n_clicks_list: List of click counts for all layer cards
        visible_layers: List of currently visible layer keys
        district: Name of the current district

    Returns:
        tuple: (updated map figure, updated visible layers list, icon styles, card classes)
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
    updated_figure = create_single_district_map(district, scatters if scatters else None)

    plus_styles, minus_styles, card_classes = handle_card_styles(visible_layers)

    return updated_figure, visible_layers, plus_styles, minus_styles, card_classes

def handle_card_styles(visible_layers):
    """
        Generate icon styles and card classes based on layer visibility.

        Args:
            visible_layers: List of visible layers to decide which icons to shows and classes to use

        Returns:
            tuple: (plus icon styles, minus icon styles, card classes)
        """
    plus_styles = []
    minus_styles = []
    card_classes = []

    for dataset_key, config in DATASET_CONFIGS.items():
        layer_key = config["layer_key"]
        is_visible = layer_key in visible_layers

        plus_styles.append({"display": "none"} if is_visible else {"display": "block"})
        minus_styles.append({"display": "block"} if is_visible else {"display": "none"})
        card_classes.append("info-card-selected" if is_visible else "")
    return plus_styles, minus_styles, card_classes
