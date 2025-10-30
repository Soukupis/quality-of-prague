import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, List
from .district_map_config import DistrictMapStyle

class MapLayerBuilder:
    def __init__(self, style: DistrictMapStyle = None):
        self.style = style or DistrictMapStyle()

    def create_choropleth_layer(self, geojson: Dict, df: pd.DataFrame, hover_info: str) -> go.Choroplethmap:
        return go.Choroplethmap(
            geojson=geojson,
            locations=df["id"],
            z=df.index,
            hoverinfo=hover_info,
            showscale=False,
            marker=dict(line=dict(width=self.style.border_width, color=self.style.border_color)),
            colorscale=[[0, self.style.background_color], [1, self.style.background_color]],
            selectedpoints=[],
        )

    def create_text_layer(self, centroids, labels: List[str]) -> go.Scattermap:
        return go.Scattermap(
            lon=centroids.x,
            lat=centroids.y,
            mode="text",
            text=labels,
            textfont=dict(size=self.style.text_size, color=self.style.text_color),
            hoverinfo="skip",
            showlegend=False,
            hovertemplate="",
        )

    def create_highlight_layer(self) -> go.Scattermap:
        return go.Scattermap(
            lon=[], lat=[],
            mode="lines",
            line=dict(width=self.style.highlight_width, color=self.style.highlight_color),
            hoverinfo="skip",
            showlegend=False,
            name="border-highlight",
            hovertemplate="",
        )