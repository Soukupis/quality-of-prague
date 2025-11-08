from utils.districts.district_utils import get_points_in_district
from utils.scatter.scatter_configs import SCATTER_LAYER_CONFIGS

def build_scatter_config(district: str, layer_keys: list) -> dict:
    """
    Build scatter point configuration for specified layers using cached loaders.

    Args:
        district: Name of the district to filter loaders for
        layer_keys: List of layer keys to include (e.g., ['parking_meters', 'police_stations', ...])

    Returns:
        Dictionary of scatter configurations for the requested layers
    """
    if not layer_keys:
        return {}

    # Build scatter config only for requested layers
    scatters = {}
    for layer_key in layer_keys:
        if layer_key in SCATTER_LAYER_CONFIGS:
            config = SCATTER_LAYER_CONFIGS[layer_key]
            filtered_data = get_points_in_district(district, layer_key)

            scatters[layer_key] = {
                "loaders": filtered_data,
                "lon_column": "geometry",
                "lat_column": "geometry",
                "marker_size": config["marker_size"],
                "marker_color": config["marker_color"],
                "marker_opacity": config["marker_opacity"],
                "name": config["name"],
            }
    return scatters