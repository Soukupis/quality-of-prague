import plotly.graph_objects as go
from .district_map_builder import DistrictMapBuilder, load_and_prepare_data
from src.configs import DATA_PATHS
from .district_map_config import SingleDistrictMapLayout, DistrictMapStyle,DistrictMapLayout
from src.utils.scatter import build_subway_entrance_traces

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

def create_single_district_map(district: str, scatters = None, polygons = None, showlegend: bool = True) -> go.Figure:
    map_builder = get_single_district_map_builder(district)

    if scatters is not None:
        for scatter_key, scatter_config in scatters.items():
            if scatter_config.get("type") == "subway_entrances":
                subway_traces = build_subway_entrance_traces(scatter_config["data"])
                for trace in subway_traces:
                    map_builder.custom_traces.append(trace)
            else:
                map_builder.add_scatter_points(
                    data=scatter_config["data"],
                    lon_column=scatter_config["lon_column"],
                    lat_column=scatter_config["lat_column"],
                    marker_size=scatter_config["marker_size"],
                    marker_color=scatter_config["marker_color"],
                    marker_opacity=scatter_config["marker_opacity"],
                    show_legend=True,
                    legend_group=scatter_config["legend_group"],
                    name=scatter_config["name"],
                )
    if polygons is not None:
        for polygon_key, polygon_config in polygons.items():
            map_builder.add_polygon_layer(
                geojson = polygon_config["geojson"],
                df = polygon_config["df"],
                background_color=polygon_config["background_color"],
                legend_group=polygon_config["legend_group"],
                name=polygon_config["name"],
            )

    return map_builder.create_map(map_builder.df, map_builder.centroids, map_builder.geojson, showlegend)




