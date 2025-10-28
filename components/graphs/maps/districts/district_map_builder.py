import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import read_file
from utils.geospatial_utils import compute_centroids, geodata_to_geojson_dict, calculate_center
from .district_map_config import DistrictMapStyle, DistrictMapLayout
from .district_map_layers import MapLayerBuilder


def load_and_prepare_data(file_path: str, name_column: str = "nazev_1") -> tuple:
    df = read_file(file_path)
    df[name_column] = df[name_column].fillna("Unknown").astype(str).str.strip()
    centroids = compute_centroids(df, projected_epsg=5514)
    geojson = geodata_to_geojson_dict(df)

    df["id"] = df.index
    df["name"] = df[name_column]

    return df, centroids, geojson


class DistrictMapBuilder:
    def __init__(self, style: DistrictMapStyle = None, layout: DistrictMapLayout = None):
        self.style = style or DistrictMapStyle()
        self.layout = layout or DistrictMapLayout()
        self.layer_builder = MapLayerBuilder(self.style)

    def create_map(self, df: pd.DataFrame, centroids, geojson: dict) -> go.Figure:
        fig = go.Figure()

        fig.add_trace(self.layer_builder.create_choropleth_layer(geojson, df))
        fig.add_trace(self.layer_builder.create_text_layer(centroids, df["name"]))
        fig.add_trace(self.layer_builder.create_highlight_layer())

        center = calculate_center(df)
        fig.update_layout(
            map=dict(style=self.layout.style, center=center, zoom=self.layout.zoom),
            height=self.layout.height,
            width=self.layout.width,
            margin=self.layout.margin,
            clickmode="event+select",
            selectionrevision=True,
            dragmode="select"
        )

        return fig