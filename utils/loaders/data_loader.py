import geopandas as gpd
from utils.cache import cached

@cached()
def read_file(location):
    return gpd.read_file(location)
