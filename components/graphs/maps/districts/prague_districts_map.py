import plotly.graph_objects as go
from .district_map_builder import DistrictMapBuilder, load_and_prepare_data
from data_config import DATA_PATHS
from .district_map_config import SingleDistrictMapLayout, DistrictMapStyle,DistrictMapLayout


def create_prague_map() -> go.Figure:
    builder = DistrictMapBuilder(DistrictMapStyle(), DistrictMapLayout(), "event+select", "select", True)
    df, centroids, geojson = load_and_prepare_data(DATA_PATHS.get_path("prague_districts"))
    return builder.create_map(df, centroids, geojson)

def create_single_district_map(district: str) -> go.Figure:
    builder = DistrictMapBuilder(DistrictMapStyle(), SingleDistrictMapLayout(), None, None, False)
    df, centroids, geojson = load_and_prepare_data(DATA_PATHS.get_path("prague_districts"))
    selected_district = df[df["nazev_1"] == district]
    selected_centroids = centroids.loc[selected_district.index]
    selected_geojson = {
        "type": "FeatureCollection",
        "features": [feature for feature in geojson["features"] if feature["properties"]["nazev_1"] == district]
    }

    return builder.create_map(selected_district, selected_centroids, selected_geojson)