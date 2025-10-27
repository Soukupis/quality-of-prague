import json
import geopandas as gpd
import pandas as pd

def compute_centroids(df: gpd.GeoDataFrame, projected_epsg=5514):
    """
    Computes centroids in a projected CRS to avoid distortion.

    Parameters:
        df: GeoDataFrame in any CRS
        projected_epsg: EPSG code for centroid calculation (meters)

    Returns:
        df_back: GeoDataFrame returned to original CRS
        centroids: Centroid coordinates in WGS84 (EPSG:4326)
    """
    # Save original CRS before transformation
    original_crs = df.crs

    # Project to meters for accurate centroids
    df_projected = df.to_crs(projected_epsg)
    centroids = df_projected.geometry.centroid

    # Convert geometry & centroids back for Plotly
    centroids = centroids.to_crs(original_crs)

    return centroids


def geodf_to_geojson_dict(df: gpd.GeoDataFrame):
    """
    Converts GeoDataFrame to GeoJSON dict for Plotly support.

    Returns:
        A Python dict compliant with GeoJSON format
    """
    return json.loads(df.to_json())

def calculate_center(df: pd.DataFrame):
    """
    Calculates the center of the GeoDataFrame's bounding box.

    Parameters:
        df: GeoDataFrame in any CRS

    Returns:
        center: dict with 'lat' and 'lon' keys
    """
    bounds = df.total_bounds
    center = dict(lat=(bounds[1] + bounds[3]) / 2, lon=(bounds[0] + bounds[2]) / 2)
    return center