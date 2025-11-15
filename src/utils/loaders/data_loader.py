from importlib import resources
import geopandas as gpd
from src.utils.cache import cached

PKG_NAME = "data"

@cached()
def read_file(name: str):
    """
    Load a GeoJSON file from the package data directory.

    Args:
        name: Relative path to the data file (e.g., 'mestske_casti/mestske_casti.geojson')

    Returns:
        GeoDataFrame containing the spatial data
    """
    ref = resources.files(PKG_NAME) / name
    with resources.as_file(ref) as file:
        gdf = gpd.read_file(file)
        return gdf


