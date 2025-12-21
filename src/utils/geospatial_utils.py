import json
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape, GeometryCollection

def compute_centroids(data: gpd.GeoDataFrame, projected_epsg=5514):
    """Compute geographic centroids using projected coordinates.

    Calculates centroids in a projected coordinate reference system (CRS)
    to avoid distortion from geographic coordinates. The function temporarily
    projects the data to a meter-based CRS, computes centroids, then converts
    back to the original CRS.

    Args:
        data: GeoDataFrame containing geometries in any CRS.
        projected_epsg: EPSG code for projected CRS used in centroid calculation.
            Default is 5514 (S-JTSK / Krovak East North), suitable for Czech Republic.

    Returns:
        GeoSeries containing centroid geometries in the original CRS of the input data.

    Examples:
        >>> import geopandas as gpd
        >>> gdf = gpd.read_file("districts.geojson")
        >>> centroids = compute_centroids(gdf)
        >>> print(centroids.head())
    """
    # Save original CRS before transformation
    original_crs = data.crs

    # Project to meters for accurate centroids
    data_projected = data.to_crs(projected_epsg)
    centroids = data_projected.geometry.centroid

    # Convert geometry & centroids back for Plotly
    centroids = centroids.to_crs(original_crs)

    return centroids


def geodata_to_geojson_dict(data: gpd.GeoDataFrame):
    """Convert GeoDataFrame to GeoJSON dictionary format.

    Transforms a GeoDataFrame into a Python dictionary compliant with the
    GeoJSON specification, making it compatible with Plotly and other
    JavaScript mapping libraries.

    Args:
        data: GeoDataFrame to convert to GeoJSON format.

    Returns:
        dict: Python dictionary in GeoJSON format with 'type', 'features',
            and 'crs' keys following the GeoJSON specification.

    Examples:
        >>> import geopandas as gpd
        >>> gdf = gpd.read_file("data.geojson")
        >>> geojson_dict = geodata_to_geojson_dict(gdf)
        >>> print(geojson_dict['type'])  # 'FeatureCollection'
    """
    return json.loads(data.to_json())

def calculate_center(data: pd.DataFrame):
    """Calculate the geographic center of a GeoDataFrame's bounding box.

    Computes the center point by finding the midpoint of the minimum bounding
    rectangle (total_bounds) of all geometries in the GeoDataFrame. This is
    useful for centering maps on the data extent.

    Args:
        data: GeoDataFrame containing spatial geometries.

    Returns:
        dict: Dictionary with 'lat' and 'lon' keys containing the center
            coordinates in the same CRS as the input data.

    Examples:
        >>> import geopandas as gpd
        >>> gdf = gpd.read_file("prague_districts.geojson")
        >>> center = calculate_center(gdf)
        >>> print(f"Center: {center['lat']}, {center['lon']}")
    """
    bounds = data.total_bounds
    center = dict(lat=(bounds[1] + bounds[3]) / 2, lon=(bounds[0] + bounds[2]) / 2)
    return center

def extract_polygons(data: gpd.GeoDataFrame, polygon_key=None, name_key=None):
    """Extract and map polygon geometries from a GeoDataFrame.

    Creates a dictionary mapping names to Shapely polygon geometries from a
    GeoDataFrame. Applies a buffer(0) operation to fix any invalid geometries.

    Args:
        data: GeoDataFrame containing polygon features.
        polygon_key: Column name containing polygon geometry (GeoJSON-like dict
            or geometry objects).
        name_key: Column name to use as dictionary keys (e.g., district names).

    Returns:
        dict: Dictionary mapping name_key values to Shapely Polygon or
            MultiPolygon objects. Returns empty dict if polygon_key or
            name_key is None.

    Examples:
        >>> import geopandas as gpd
        >>> districts = gpd.read_file("districts.geojson")
        >>> polygons = extract_polygons(districts, "geometry", "district_name")
        >>> print(list(polygons.keys()))  # ['District 1', 'District 2', ...]
    """
    if polygon_key is None or name_key is None:
        return {}

    polygons = {}
    for index, row in data.iterrows():
        geom = shape(row[polygon_key]).buffer(0)
        polygons[row[name_key]] = geom
    return polygons

def is_point_within_polygon(point, polygon):
    """Check if a point is contained within a polygon.

    Determines whether a given point geometry falls within the boundaries
    of a polygon or multipolygon. Handles edge cases for empty geometries
    and geometry collections.

    Args:
        point: Shapely Point object to test.
        polygon: Shapely Polygon or MultiPolygon object to test against.

    Returns:
        bool: True if the point is within the polygon boundaries, False
            otherwise. Returns False for empty or GeometryCollection polygons.

    Examples:
        >>> from shapely.geometry import Point, Polygon
        >>> point = Point(14.4, 50.1)
        >>> polygon = Polygon([(14.0, 50.0), (15.0, 50.0), (15.0, 51.0), (14.0, 51.0)])
        >>> is_point_within_polygon(point, polygon)
        True
    """
    if polygon.is_empty or isinstance(polygon, GeometryCollection):
        return False
    return polygon.contains(point)


def points_within_polygon(polygon, data, geometry_key=None):
    """Filter points that fall within a polygon boundary.

    Returns a subset of a DataFrame containing only the point geometries
    that are spatially contained within the given polygon. Uses a boolean
    mask for efficient filtering.

    Args:
        polygon: Shapely Polygon or MultiPolygon object defining the boundary
            to filter by.
        data: DataFrame or GeoDataFrame containing point geometries.
        geometry_key: Column name containing the point geometries (Shapely
            Point objects). If None, uses the default geometry column.

    Returns:
        DataFrame or GeoDataFrame: Subset of input data containing only rows
            where the point geometry is within the polygon. Returns empty
            DataFrame if no points are found within the polygon.

    Examples:
        >>> from shapely.geometry import Polygon
        >>> import geopandas as gpd
        >>> polygon = Polygon([(14.0, 50.0), (15.0, 50.0), (15.0, 51.0), (14.0, 51.0)])
        >>> points_gdf = gpd.read_file("points.geojson")
        >>> filtered = points_within_polygon(polygon, points_gdf, "geometry")
        >>> print(len(filtered))  # Number of points within polygon
    """
    # Create a boolean mask indicating which points are within the polygon
    mask = data[geometry_key].apply(polygon.contains)
    
    # Filter and return only the rows where the point is within the polygon
    return data[mask]

def point_count_for_polygon(polygon, data, geometry_key=None):
    """Count the number of points within a polygon boundary.

    Applies a spatial containment test to count how many point geometries
    from a dataset fall within the given polygon.

    Args:
        polygon: Shapely Polygon or MultiPolygon object defining the boundary.
        data: DataFrame or GeoDataFrame containing point geometries.
        geometry_key: Column name containing the point geometries. If None,
            uses the default geometry column.

    Returns:
        int: Total number of points within the polygon boundary.

    Examples:
        >>> from shapely.geometry import Polygon
        >>> import geopandas as gpd
        >>> polygon = Polygon([(14.0, 50.0), (15.0, 50.0), (15.0, 51.0), (14.0, 51.0)])
        >>> points = gpd.read_file("metro_stations.geojson")
        >>> count = point_count_for_polygon(polygon, points, "geometry")
        >>> print(f"Found {count} points")
    """
    return data[geometry_key].apply(polygon.contains).sum()

def polygon_points_count(polygons_source, data, geometry_key=None):
    """Count points within multiple polygons.

    Calculates the number of points contained within each polygon from a
    collection of polygons. Useful for generating statistics like the number
    of facilities per district.

    Args:
        polygons_source: Dictionary mapping names to Shapely Polygon or
            MultiPolygon objects, or DataFrame containing polygon geometries.
        data: DataFrame or GeoDataFrame containing point geometries to count.
        geometry_key: Column name containing the point geometries. If None,
            uses the default geometry column.

    Returns:
        dict: Dictionary mapping polygon names to point counts (int). Only
            processes dict-type polygons_source currently.

    Examples:
        >>> from shapely.geometry import Polygon
        >>> import geopandas as gpd
        >>> districts = {"District 1": Polygon(...), "District 2": Polygon(...)}
        >>> points = gpd.read_file("facilities.geojson")
        >>> counts = polygon_points_count(districts, points, "geometry")
        >>> print(counts)  # {'District 1': 15, 'District 2': 23, ...}
    """
    polygons_count = {}

    if isinstance(polygons_source, dict):
        for name, geom in polygons_source.items():
            count = data[geometry_key].apply(geom.contains).sum()
            polygons_count[name] = count
    return polygons_count
