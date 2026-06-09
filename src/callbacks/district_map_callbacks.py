from dash import Input, Output, callback, State, ctx, exceptions, ALL
from src.components.graphs import create_single_district_map
from src.configs.data_config import DATA_PATHS
from src.utils.loaders.data_loader import read_file
from src.utils.polygons.polygon_utils import build_polygon_config
from src.utils.scatter.scatter_utils import build_scatter_config
from src.configs.dataset_config import DATASET_CONFIGS

def get_prague_districts_lookup():
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
    visible_layers = visible_layers or []

    triggered = ctx.triggered_id
    if not triggered:
        raise exceptions.PreventUpdate

    clicked_index = triggered['index']

    clicked_config = DATASET_CONFIGS.get(clicked_index)
    if not clicked_config:
        raise exceptions.PreventUpdate

    layer_key = clicked_config["layer_key"]

    if layer_key in visible_layers:
        visible_layers.remove(layer_key)
    else:
        visible_layers.append(layer_key)

    scatters = build_scatter_config(district, visible_layers)
    polygons = build_polygon_config(district, visible_layers)
    updated_figure = create_single_district_map(district, scatters if scatters else None, polygons if polygons else None)

    plus_styles, minus_styles, card_classes = handle_card_styles(visible_layers)

    return updated_figure, visible_layers, plus_styles, minus_styles, card_classes

def handle_card_styles(visible_layers):
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
