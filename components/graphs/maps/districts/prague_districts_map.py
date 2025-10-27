import plotly.graph_objects as go
from .district_map_builder import DistrictMapBuilder, load_and_prepare_data
from data_config import DATA_PATHS


def create_prague_map() -> go.Figure:
    builder = DistrictMapBuilder()
    df, centroids, geojson = load_and_prepare_data(DATA_PATHS.get_path("prague_districts"))
    return builder.create_map(df, centroids, geojson)