from src.utils.cache import cached
from src.utils.loaders.districts_loader import get_districts_data
from src.utils.geospatial_utils import extract_polygons, points_within_polygon
from src.configs.dataset_config import DATASET_CONFIGS

@cached(timeout=300)
def get_district_polygons():
    districts = get_districts_data()
    return extract_polygons(districts, "geometry", "nazev_1")


def get_single_district_polygon(district_name):
    polygons = get_district_polygons()

    if district_name not in polygons:
        return None

    return polygons[district_name]

@cached(timeout=300)
def get_district_areas_km2() -> dict:
    districts = get_districts_data()
    projected = districts.to_crs(5514)
    projected["area_km2"] = projected.geometry.area / 1_000_000
    return dict(zip(districts["nazev_1"], projected["area_km2"]))


@cached()
def get_points_in_district(district: str, layer_type: str):
    layer_loader_fn = DATASET_CONFIGS[layer_type]["loader_function"]
    data = layer_loader_fn()
    district_polygon = get_single_district_polygon(district)

    return points_within_polygon(district_polygon, data, "geometry")

