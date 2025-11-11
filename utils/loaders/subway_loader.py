import geopandas as gpd
import numpy as np
from utils.cache import cached
from data_config import DATA_PATHS


@cached()
def load_subway_entrances():
    """Load metro entrances GeoJSON data."""
    return gpd.read_file(DATA_PATHS.subway_entrances)


@cached()
def aggregate_metro_stations(df):
    """
    Aggregate metro entrance points by station name (uzel_nazev).

    Returns aggregated dataframe with:
    - uzel_nazev: Station name
    - geometry: List of all entrance point geometries
    - vst_linka: Comma-separated unique lines serving the station
    """
    aggregated = df.groupby(["uzel_nazev"]).agg({
        "geometry": list,
        "vst_linka": lambda x: ",".join(sorted(set(",".join(x).replace(" ", "").split(","))))
    }).reset_index()

    return aggregated


def get_transfer_stations(df):
    """Get all transfer stations (stations with multiple lines)."""
    return df[df["vst_linka"].str.contains(",", na=False)]


def get_single_line_stations(df, line):
    """Get all stations for a single metro line (A, B, or C)."""
    return df[df["vst_linka"] == line]


def calculate_station_circle_params(geometry_list, buffer_multiplier=1.2):
    """
    Calculate center point and radius for a station's entrance circle.

    Args:
        geometry_list: List of Point geometries for station entrances
        buffer_multiplier: Multiplier for radius to add buffer around points

    Returns:
        tuple: (center_lon, center_lat, radius, lat_scale)
    """
    lons = [point.x for point in geometry_list]
    lats = [point.y for point in geometry_list]

    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)

    # Calculate max distance accounting for lat/lon scale
    lat_scale = np.cos(np.radians(center_lat))
    max_dist = 0

    for lon, lat in zip(lons, lats):
        dist = np.sqrt(((lon - center_lon) * lat_scale)**2 + (lat - center_lat)**2)
        max_dist = max(max_dist, dist)

    radius = max_dist * buffer_multiplier

    return center_lon, center_lat, radius, lat_scale

