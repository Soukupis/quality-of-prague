from utils.cache import cached
from utils.loaders.districts_loader import get_districts_data, get_police_stations_data, get_parking_meters_data
from utils.geospatial_utils import extract_polygons, points_within_polygon
from dataset_config import DATASET_CONFIGS

@cached(timeout=300)
def get_district_polygons():
    """
    Get all district polygons from the districts data.

    Returns:
        dict: Dictionary mapping district names to their polygon geometries
    """
    districts = get_districts_data()
    return extract_polygons(districts, "geometry", "nazev_1")


def get_single_district_polygon(district_name):
    """
    Get the polygon geometry for a specific district.

    Args:
        district_name: Name of the district

    Returns:
        Polygon geometry for the district, or None if district not found
    """
    polygons = get_district_polygons()

    if district_name not in polygons:
        return None

    return polygons[district_name]

@cached()
def get_points_in_district(district: str, layer_type: str):
    """
    Get points within a district boundary - cached by district and layer type.

    Args:
        district: District name
        layer_type: type of layer we want to get the points for (e.g., 'police_stations', 'parking_meters')

    Returns:
        Filtered geodataframe of points within the district
    """
    layer_loader_fn = DATASET_CONFIGS[layer_type]["loader_function"]
    data = layer_loader_fn()
    district_polygon = get_single_district_polygon(district)

    return points_within_polygon(district_polygon, data, "geometry")

