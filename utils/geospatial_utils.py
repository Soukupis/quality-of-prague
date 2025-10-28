import json
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape, GeometryCollection

def compute_centroids(data: gpd.GeoDataFrame, projected_epsg=5514):
    """
    Computes centroids in a projected CRS to avoid distortion.

    Parameters:
        data: GeoDataFrame in any CRS
        projected_epsg: EPSG code for centroid calculation (meters)

    Returns:
        data_back: GeoDataFrame returned to original CRS
        centroids: Centroid coordinates in WGS84 (EPSG:4326)
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
    """
    Converts GeoDataFrame to GeoJSON dict for Plotly support.

    Returns:
        A Python dict compliant with GeoJSON format
    """
    return json.loads(data.to_json())

def calculate_center(data: pd.DataFrame):
    """
    Calculates the center of the GeoDataFrame's bounding box.

    Parameters:
        data: GeoDataFrame in any CRS

    Returns:
        center: dict with 'lat' and 'lon' keys
    """
    bounds = data.total_bounds
    center = dict(lat=(bounds[1] + bounds[3]) / 2, lon=(bounds[0] + bounds[2]) / 2)
    return center

def extract_polygons(data: gpd.GeoDataFrame, polygon_key=None, name_key=None):
    """
    Extracts polygons from a GeoDataFrame and returns a dictionary mapping names to polygon geometries.

    Parameters:
        data: GeoDataFrame containing polygon data
        polygon_key: column name containing polygon geometry (as GeoJSON-like dict)
        name_key: column name to use as dictionary keys (e.g., district name)

    Returns:
        polygons: dict mapping name_key values to shapely Polygon objects
    """
    if polygon_key is None or name_key is None:
        return {}

    polygons = {}
    for index, row in data.iterrows():
        geom = shape(row[polygon_key]).buffer(0)
        polygons[row[name_key]] = geom
    return polygons

def is_point_within_polygon(point, polygon):
    """
    Checks if a given point is within a polygon.

    Parameters:
        point: shapely Point object
        polygon: shapely Polygon or MultiPolygon object

    Returns:
        bool: True if point is within polygon, False otherwise
    """
    if polygon.is_empty or isinstance(polygon, GeometryCollection):
        return False
    return polygon.contains(point)


def point_count_for_polygon(polygon, data, geometry_key=None):
    """
    Counts the number of points within a given polygon.

    Parameters:
        polygon: shapely Polygon or MultiPolygon object
        data: DataFrame with point geometries
        geometry_key: column for point geometries in data

    Returns:
        count: int number of points within the polygon
    """
    return data[geometry_key].apply(polygon.contains).sum()

def polygon_points_count(polygons_source, data, geometry_key=None):
    """
    Counts the number of points within each polygon, dynamically using provided keys.

    Parameters:
        polygons_source: dict or DataFrame containing polygons
        data: DataFrame with point geometries
        geometry_key: column for point geometries in data

    Returns:
        polygons_count: dict mapping name to count
    """
    polygons_count = {}

    if isinstance(polygons_source, dict):
        for name, geom in polygons_source.items():
            count = data[geometry_key].apply(geom.contains).sum()
            polygons_count[name] = count
    return polygons_count
