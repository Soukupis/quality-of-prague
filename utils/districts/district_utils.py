from utils.cache import cached
from utils.loaders.districts_loader import get_districts_data, get_police_stations_data, get_parking_meters_data
from utils.geospatial_utils import extract_polygons, points_within_polygon

@cached(timeout=300)
def get_district_polygons():
    districts = get_districts_data()
    return extract_polygons(districts, "geometry", "nazev_1")


def get_single_district_polygon(district_name):
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
        layer_type: 'police_stations' or 'parking_meters'

    Returns:
        Filtered geodataframe of points within the district
    """
    polygons = get_district_polygons()
    district_polygon = get_single_district_polygon(district)

    if layer_type == 'police_stations':
        data = get_police_stations_data()
    elif layer_type == 'parking_meters':
        data = get_parking_meters_data()
    else:
        raise ValueError(f"Unknown layer type: {layer_type}")

    return points_within_polygon(district_polygon, data, "geometry")

