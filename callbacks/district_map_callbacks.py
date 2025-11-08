from dash import Input, Output, callback, State,ctx, exceptions
from components.graphs.maps.districts import create_single_district_map
from data_config import DATA_PATHS
from utils.loaders.data_loader import read_file
from utils.scatter.scatter_utils import build_scatter_config

def get_prague_districts_lookup():
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
    if click_data and click_data.get("points"):
        location_id = click_data["points"][0]["location"]
        lookup_df = get_prague_districts_lookup()
        district_row = lookup_df[lookup_df["id"] == location_id]
        if not district_row.empty:
            district_name = district_row["name"].iloc[0]
            return "/districts/district-detail" + f"?district={district_name}"
        else:
            raise exceptions.PreventUpdate
    raise exceptions.PreventUpdate

@callback(
    [Output('single-district-map', 'figure', allow_duplicate=True),
     Output('police-stations-plus-icon', 'style', allow_duplicate=True),
     Output('police-stations-minus-icon', 'style', allow_duplicate=True),
     Output('parking-meters-plus-icon', 'style', allow_duplicate=True),
     Output('parking-meters-minus-icon', 'style', allow_duplicate=True),
     Output('police-stations', 'className', allow_duplicate=True),
     Output('parking-meters', 'className', allow_duplicate=True)],
    Input('visible-layers-store', 'data'),
    State('district-store', 'data'),
    prevent_initial_call='initial_duplicate'
)
def restore_map_state(visible_layers, district):
    """
    Restore map with previously selected layers when page loads.

    This callback runs when the page first loads and reads the visible_layers
    from session storage. If there are any layers saved, it recreates the map
    with those layers visible. Also restores the correct icon states.

    Args:
        visible_layers: List of layer keys from session storage
        district: Current district name

    Returns:
        tuple: (Figure with restored layer visibility, icon styles, card classes)
    """
    if not visible_layers or not district:
        figure = create_single_district_map(district, None)
    else:
        scatters = build_scatter_config(district, visible_layers)
        figure = create_single_district_map(district, scatters if scatters else None)

    # Set icon visibility based on layer state
    visible_layers = visible_layers or []
    police_plus_style = {"display": "none"} if 'police_stations' in visible_layers else {"display": "block"}
    police_minus_style = {"display": "block"} if 'police_stations' in visible_layers else {"display": "none"}
    parking_plus_style = {"display": "none"} if 'parking_meters' in visible_layers else {"display": "block"}
    parking_minus_style = {"display": "block"} if 'parking_meters' in visible_layers else {"display": "none"}

    # Set selected class on cards
    police_class = "info-card-selected" if 'police_stations' in visible_layers else ""
    parking_class = "info-card-selected" if 'parking_meters' in visible_layers else ""

    return figure, police_plus_style, police_minus_style, parking_plus_style, parking_minus_style, police_class, parking_class

@callback(
    [Output('single-district-map', 'figure'),
     Output('visible-layers-store', 'data'),
     Output('police-stations-plus-icon', 'style'),
     Output('police-stations-minus-icon', 'style'),
     Output('parking-meters-plus-icon', 'style'),
     Output('parking-meters-minus-icon', 'style'),
     Output('police-stations', 'className'),
     Output('parking-meters', 'className')],
    [Input('police-stations', 'n_clicks'),
     Input('parking-meters', 'n_clicks')],
    [State('visible-layers-store', 'data'),
     State('district-store', 'data')],
    prevent_initial_call=True
)
def toggle_map_layer(police_clicks, parking_clicks, visible_layers, district):
    """
    Toggle visibility of map layers when info cards are clicked.

    This callback responds to clicks on the info cards (police stations, parking meters, ...)
    and updates the map to show/hide the corresponding loaders points.

    Args:
        police_clicks: Number of clicks on police stations card
        parking_clicks: Number of clicks on parking meters card
        visible_layers: List of currently visible layer keys
        district: Name of the current district

    Returns:
        tuple: (updated map figure, updated visible layers list, icon styles, card classes)
    """

    layer_map = {
        'police-stations': 'police_stations',
        'parking-meters': 'parking_meters'
    }

    # Get which card was clicked using ctx.triggered_id
    clicked_card = ctx.triggered_id

    if clicked_card and clicked_card in layer_map:
        layer_key = layer_map[clicked_card]

        # Toggle the layer: remove if visible, add if hidden
        if layer_key in visible_layers:
            visible_layers.remove(layer_key)
        else:
            visible_layers.append(layer_key)

    scatters = build_scatter_config(district, visible_layers)

    # Create the updated map with only visible layers
    updated_figure = create_single_district_map(district, scatters if scatters else None)

    # Set icon visibility based on layer state
    police_plus_style = {"display": "none"} if 'police_stations' in visible_layers else {"display": "block"}
    police_minus_style = {"display": "block"} if 'police_stations' in visible_layers else {"display": "none"}
    parking_plus_style = {"display": "none"} if 'parking_meters' in visible_layers else {"display": "block"}
    parking_minus_style = {"display": "block"} if 'parking_meters' in visible_layers else {"display": "none"}

    # Set selected class on cards
    police_class = "info-card-selected" if 'police_stations' in visible_layers else ""
    parking_class = "info-card-selected" if 'parking_meters' in visible_layers else ""

    return updated_figure, visible_layers, police_plus_style, police_minus_style, parking_plus_style, parking_minus_style, police_class, parking_class

