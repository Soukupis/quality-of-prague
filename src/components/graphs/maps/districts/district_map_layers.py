"""Map layer creation utilities for district visualizations.

This module provides the MapLayerBuilder class for creating various Plotly map
layers including choropleth districts, text labels, scatter points, polygons,
and highlight effects. Used internally by DistrictMapBuilder.

Classes:
    MapLayerBuilder: Factory for creating Plotly map trace objects
"""
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List
from .district_map_config import DistrictMapStyle

class MapLayerBuilder:
    """Factory class for creating Plotly map layer traces.

    Provides methods to create different types of map layers (choropleth,
    scatter, text, polygons) with consistent styling. Used internally by
    DistrictMapBuilder to construct complete map visualizations.

    Attributes:
        style: DistrictMapStyle instance defining colors and styling.

    Examples:
        >>> style = DistrictMapStyle()
        >>> builder = MapLayerBuilder(style)
        >>> choropleth = builder.create_choropleth_layer(geojson, df, "text")
    """

    def __init__(self, style = None):
        """Initialize the MapLayerBuilder with optional styling.

        Args:
            style: DistrictMapStyle instance for styling layers. If None,
                uses default DistrictMapStyle().
        """
        self.style = style or DistrictMapStyle()

    def create_choropleth_layer(self, geojson: Dict, df: pd.DataFrame, hover_info: str) -> go.Choroplethmap:
        """Create a choropleth map layer for district boundaries.

        Builds the base district polygon layer with uniform coloring and
        border styling. Used as the foundation layer for district maps.

        Args:
            geojson: GeoJSON dictionary containing district geometries.
            df: DataFrame with district data, must have 'id' column.
            hover_info: Plotly hover info mode (e.g., "text", "skip").

        Returns:
            go.Choroplethmap: Plotly choropleth trace for district boundaries.

        Examples:
            >>> choropleth = builder.create_choropleth_layer(
            ...     geojson=district_geojson,
            ...     df=district_df,
            ...     hover_info="text"
            ... )
        """
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

    @staticmethod
    def create_polygon_layer(
            geojson: Dict,
            df: pd.DataFrame,
            background_color: str = "red",
            legend_group: str = None,
            show_legend: bool = True,
            name: str = None,
    ) -> go.Choroplethmap:
        """Create a polygon overlay layer (e.g., parking zones).

        Builds a choropleth layer for polygon overlays like parking zones or
        restricted areas. Can be grouped in legend and colored independently.

        Args:
            geojson: GeoJSON dictionary containing polygon geometries.
            df: DataFrame with polygon data, must have 'id' column.
            background_color: Fill color for polygons. Defaults to "red".
            legend_group: Group name for legend organization. Defaults to None.
            show_legend: Whether to show in legend. Defaults to True.
            name: Display name for the layer. Defaults to None.

        Returns:
            go.Choroplethmap: Plotly choropleth trace for polygon overlay.

        Examples:
            >>> polygon_layer = MapLayerBuilder.create_polygon_layer(
            ...     geojson=zones_geojson,
            ...     df=zones_df,
            ...     background_color='rgba(255, 0, 0, 0.3)',
            ...     name='Paid Parking Zones'
            ... )
        """
        trace_params = dict(
            geojson=geojson,
            locations=df["id"],
            z=df.index,
            showscale=False,
            colorscale=[[0, background_color], [1, background_color]],
            legendgroup=legend_group,
            legendgrouptitle=dict(text=legend_group),
            showlegend = show_legend,
            hoverinfo="skip",
        )

        if name:
            trace_params['name'] = name

        return go.Choroplethmap(**trace_params)

    def create_text_layer(self, centroids, labels: List[str]) -> go.Scattermap:
        """Create a text label layer for district names.

        Builds a scatter map layer displaying text labels at district centroids.
        Labels are positioned at the geographic center of each district for
        optimal readability.

        Args:
            centroids: GeoSeries of Point geometries indicating label positions.
            labels: List of text labels (district names) to display.

        Returns:
            go.Scattermap: Plotly scatter trace with text mode for labels.

        Examples:
            >>> text_layer = builder.create_text_layer(
            ...     centroids=district_centroids,
            ...     labels=["Praha 1", "Praha 2", "Praha 3"]
            ... )
        """
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
        """Create an empty highlight layer for selected districts.

        Creates a scatter layer initialized with empty data, used to highlight
        district boundaries when districts are selected. The layer can be
        updated dynamically with coordinates to show selection.

        Returns:
            go.Scattermap: Empty Plotly scatter trace for highlighting borders.

        Examples:
            >>> highlight = builder.create_highlight_layer()
            >>> # Later updated with coordinates to show selection
        """
        return go.Scattermap(
            lon=[], lat=[],
            mode="lines",
            line=dict(width=self.style.highlight_width, color=self.style.highlight_color),
            hoverinfo="skip",
            showlegend=False,
            name="border-highlight",
            hovertemplate="",
        )

    @staticmethod
    def create_scatter_layer(
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
        legend_group: str = None,
        name: str = None,
    ) -> go.Scattermap:
        """Create a scatter point layer for map features.

        Builds a scatter map layer displaying point features like parking meters,
        metro stations, or police stations. Supports both simple coordinate
        columns and geometry columns with x/y attributes.

        Args:
            data: DataFrame containing point data.
            lon_column: Column name for longitude values or geometry objects
                with x attribute. Defaults to "lon".
            lat_column: Column name for latitude values or geometry objects
                with y attribute. Defaults to "lat".
            hover_text_column: Column containing hover text for points.
                Defaults to "hover_text".
            marker_size: Size of markers in pixels. Defaults to 9.
            marker_color: Color for markers (CSS color or hex). Defaults to "blue".
            marker_opacity: Opacity of markers (0-1). Defaults to 0.8.
            mode: Plotly scatter mode (e.g., "markers", "lines+markers").
                Defaults to "markers".
            hover_info: Plotly hover info mode. Defaults to "text".
            show_legend: Whether to show in legend. Defaults to False.
            legend_group: Group name for legend organization. Defaults to None.
            name: Display name for this layer. Defaults to None.

        Returns:
            go.Scattermap: Plotly scatter trace for point features.

        Examples:
            >>> scatter = MapLayerBuilder.create_scatter_layer(
            ...     data=parking_df,
            ...     lon_column='geometry',
            ...     lat_column='geometry',
            ...     marker_color='#8B008B',
            ...     marker_size=10,
            ...     name='Parking Meters'
            ... )
        """

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
            legendgroup=legend_group,
            legendgrouptitle=dict(text=legend_group)
        )

        if hover_text_column and hover_text_column in data.columns:
            trace_params['text'] = data[hover_text_column]

        if name:
            trace_params['name'] = name

        return go.Scattermap(**trace_params)

