from src.utils.cache import cached
from src.utils.loaders.districts_loader import get_districts_data
from src.utils.geospatial_utils import extract_polygons, points_within_polygon
from src.configs.dataset_config import DATASET_CONFIGS

@cached(timeout=300)
def get_district_polygons():
    """Get all district polygon geometries as a dictionary.

    Retrieves district data and extracts polygon geometries, mapping district
    names to their corresponding Shapely polygon objects. Results are cached
    for 5 minutes (300 seconds) to improve performance.

    Returns:
        dict: Dictionary mapping district names (str) to Shapely Polygon or
            MultiPolygon geometries.

    Examples:
        >>> polygons = get_district_polygons()
        >>> print(list(polygons.keys()))  # ['Praha 1', 'Praha 2', ...]
        >>> praha1 = polygons['Praha 1']
        >>> print(type(praha1))  # <class 'shapely.geometry.polygon.Polygon'>
    """
    districts = get_districts_data()
    return extract_polygons(districts, "geometry", "nazev_1")


def get_single_district_polygon(district_name):
    """Get the polygon geometry for a specific district.

    Retrieves the Shapely polygon geometry for a named district from the
    cached district polygons dictionary.

    Args:
        district_name: Name of the district (e.g., "Praha 1", "Praha 2").

    Returns:
        Shapely Polygon or MultiPolygon geometry for the district, or None
            if the district name is not found.

    Examples:
        >>> polygon = get_single_district_polygon("Praha 1")
        >>> if polygon:
        ...     print(f"Area: {polygon.area}")
        >>> else:
        ...     print("District not found")
    """
    polygons = get_district_polygons()

    if district_name not in polygons:
        return None

    return polygons[district_name]

@cached()
def get_points_in_district(district: str, layer_type: str):
    """Get all points of a specific layer type within a district boundary.

    Filters point data by district boundaries using spatial operations. Loads
    the appropriate dataset based on layer_type, retrieves the district polygon,
    and returns only points falling within that polygon. Results are cached for
    performance.

    Args:
        district: Name of the district (e.g., "Praha 1", "Praha 2").
        layer_type: Type of layer to retrieve points for. Must be a key in
            DATASET_CONFIGS (e.g., 'police_stations', 'parking_meters',
            'metro_entrances').

    Returns:
        GeoDataFrame: Filtered GeoDataFrame containing only points within the
            specified district boundary. Returns empty GeoDataFrame if no
            points are found or if district doesn't exist.

    Examples:
        >>> # Get all police stations in Praha 1
        >>> stations = get_points_in_district("Praha 1", "police_stations")
        >>> print(f"Found {len(stations)} police stations")
        >>>
        >>> # Get parking meters in Praha 2
        >>> meters = get_points_in_district("Praha 2", "parking_meters")
        >>> print(meters.head())
    """
    layer_loader_fn = DATASET_CONFIGS[layer_type]["loader_function"]
    data = layer_loader_fn()
    district_polygon = get_single_district_polygon(district)

    return points_within_polygon(district_polygon, data, "geometry")

