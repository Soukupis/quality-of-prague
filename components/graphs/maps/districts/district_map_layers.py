import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List
from .district_map_config import DistrictMapStyle

class MapLayerBuilder:
    def __init__(self, style = None):
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

    def create_scatter_layer(
        self,
        data: pd.DataFrame,
        lon_column: str = "lon",
        lat_column: str = "lat",
        hover_text_column: str = "hover_text",
        marker_size: int = 9,
        marker_color: str = "blue",
        marker_opacity: float = 0.8,
        mode: str = "markers",
        hover_info: str = "text",
        show_legend: bool = False,
        name: str = None,
    ) -> go.Scattermap:

        if hasattr(data[lon_column].iloc[0] if len(data) > 0 else None, 'x'):
            lon_values = data[lon_column].x
            lat_values = data[lat_column].y
        else:
            lon_values = data[lon_column]
            lat_values = data[lat_column]

        trace_params = dict(
            lon=lon_values,
            lat=lat_values,
            mode=mode,
            marker=dict(
                size=marker_size,
                color=marker_color,
                opacity=marker_opacity,
                symbol="circle"
            ),
            hoverinfo=hover_info,
            showlegend=show_legend,
        )

        if hover_text_column and hover_text_column in data.columns:
            trace_params['text'] = data[hover_text_column]

        if name:
            trace_params['name'] = name

        return go.Scattermap(**trace_params)

