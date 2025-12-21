from importlib import resources
import geopandas as gpd
from src.utils.cache import cached

PKG_NAME = "data"

@cached()
def read_file(name: str):
    """Load a GeoJSON file from the package data directory.

    Reads a GeoJSON file using importlib.resources to access package data
    files reliably across different installation methods. Results are cached
    to improve performance on repeated access.

    Args:
        name: Relative path to the data file from the 'data' package root
            (e.g., 'mestske_casti/mestske_casti.geojson',
            'parkovaci_automaty/parkovaci_automaty.geojson').

    Returns:
        GeoDataFrame: GeoPandas GeoDataFrame containing the spatial data
            loaded from the GeoJSON file.

    Examples:
        >>> # Load districts data
        >>> districts = read_file('mestske_casti/mestske_casti.geojson')
        >>> print(districts.head())
        >>>
        >>> # Load parking meters
        >>> parking = read_file('parkovaci_automaty/parkovaci_automaty.geojson')
        >>> print(f"Found {len(parking)} parking meters")
    """
    ref = resources.files(PKG_NAME) / name
    with resources.as_file(ref) as file:
        gdf = gpd.read_file(file)
        return gdf


