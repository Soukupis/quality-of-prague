from src.utils.districts import get_points_in_district
from src.utils.geospatial_utils import geodata_to_geojson_dict
from .polygons_configs import POLYGON_LAYERS_CONFIGS


def build_polygon_config(district: str, layer_keys: list) -> dict:
    if not layer_keys:
        return {}

    polygons = {}

    for layer_key in layer_keys:
        if layer_key in POLYGON_LAYERS_CONFIGS:
            config = POLYGON_LAYERS_CONFIGS[layer_key]
            df, geojson = load_and_prepare_polygon_data(district, layer_key)

            polygons[layer_key] = {
                "geojson": geojson,
                "df": df,
                "background_color": config["background_color"],
                'legend_group': config['legend_group'],
                'name': config['name'],
            }
    return polygons


def load_and_prepare_polygon_data(district: str, layer_key: str) -> tuple:
    df = get_points_in_district(district, layer_key)
    geojson = geodata_to_geojson_dict(df)

    df["id"] = df.index
    return df, geojson

