import plotly.graph_objects as go
from .district_map_builder import DistrictMapBuilder, load_and_prepare_data
from data_config import DATA_PATHS
from .district_map_config import SingleDistrictMapLayout, DistrictMapStyle,DistrictMapLayout

def get_single_district_map_builder(district: str) -> DistrictMapBuilder:
    builder = DistrictMapBuilder(DistrictMapStyle(), SingleDistrictMapLayout(), None, None, False, "skip")
    df, centroids, geojson = load_and_prepare_data(DATA_PATHS.get_path("prague_districts"))
    selected_district = df[df["nazev_1"] == district]
    selected_centroids = centroids.loc[selected_district.index]
    selected_geojson = {
        "type": "FeatureCollection",
        "features": [feature for feature in geojson["features"] if feature["properties"]["nazev_1"] == district]
    }

    builder.df = selected_district
    builder.centroids = selected_centroids
    builder.geojson = selected_geojson

    return builder

def create_prague_map() -> go.Figure:
    builder = DistrictMapBuilder(DistrictMapStyle(), DistrictMapLayout(), "event+select", "select", True, "text")
    df, centroids, geojson = load_and_prepare_data(DATA_PATHS.get_path("prague_districts"))
    return builder.create_map(df, centroids, geojson)

def create_single_district_map(district: str, scatters = None) -> go.Figure:
    map_builder = get_single_district_map_builder(district)

    if scatters is not None:
        for scatter_key in scatters:
            map_builder.add_scatter_points(
                data=scatters[scatter_key]["loaders"],
                lon_column=scatters[scatter_key]["lon_column"],
                lat_column=scatters[scatter_key]["lat_column"],
                marker_size=scatters[scatter_key]["marker_size"],
                marker_color=scatters[scatter_key]["marker_color"],
                marker_opacity=scatters[scatter_key]["marker_opacity"],
                name=scatters[scatter_key]["name"],
            )
    return map_builder.create_map(map_builder.df, map_builder.centroids, map_builder.geojson)
