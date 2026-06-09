from importlib import resources
import geopandas as gpd
from src.utils.cache import cached

PKG_NAME = "data"

@cached()
def read_file(name: str):
    ref = resources.files(PKG_NAME) / name
    with resources.as_file(ref) as file:
        gdf = gpd.read_file(file)
        return gdf


