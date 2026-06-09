import json
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape, GeometryCollection

def compute_centroids(data: gpd.GeoDataFrame, projected_epsg=5514):
    original_crs = data.crs
    data_projected = data.to_crs(projected_epsg)
    centroids = data_projected.geometry.centroid
    centroids = centroids.to_crs(original_crs)
    return centroids


def geodata_to_geojson_dict(data: gpd.GeoDataFrame):
    return json.loads(data.to_json())

def calculate_center(data: pd.DataFrame):
    bounds = data.total_bounds
    center = dict(lat=(bounds[1] + bounds[3]) / 2, lon=(bounds[0] + bounds[2]) / 2)
    return center

def extract_polygons(data: gpd.GeoDataFrame, polygon_key=None, name_key=None):
    if polygon_key is None or name_key is None:
        return {}

    polygons = {}
    for index, row in data.iterrows():
        geom = shape(row[polygon_key]).buffer(0)
        polygons[row[name_key]] = geom
    return polygons

def is_point_within_polygon(point, polygon):
    if polygon.is_empty or isinstance(polygon, GeometryCollection):
        return False
    return polygon.contains(point)


def points_within_polygon(polygon, data, geometry_key=None):
    mask = data[geometry_key].apply(polygon.contains)
    return data[mask]

def point_count_for_polygon(polygon, data, geometry_key=None):
    return data[geometry_key].apply(polygon.contains).sum()

def polygon_points_count(polygons_source, data, geometry_key=None):
    polygons_count = {}

    if isinstance(polygons_source, dict):
        for name, geom in polygons_source.items():
            count = data[geometry_key].apply(geom.contains).sum()
            polygons_count[name] = count
    return polygons_count
