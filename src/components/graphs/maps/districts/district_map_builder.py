"""District map builder for creating interactive Prague district visualizations.

This module provides tools for building interactive Plotly maps of Prague districts
with support for choropleth layers, scatter points, polygons, and custom styling.
The DistrictMapBuilder class uses a fluent interface for adding layers.

Classes:
    DistrictMapBuilder: Main map builder with fluent API for layer management.

Functions:
    load_and_prepare_data: Load and prepare geographic data for mapping.
"""
import plotly.graph_objects as go
import pandas as pd
from src.utils.loaders.data_loader import read_file
from src.utils.geospatial_utils import compute_centroids, geodata_to_geojson_dict, calculate_center
from .district_map_layers import MapLayerBuilder
from typing import Dict

def load_and_prepare_data(file_path: str, name_column: str = "nazev_1") -> tuple:
    """Load geographic data and prepare it for mapping.

    Reads a GeoJSON file, computes centroids, converts to GeoJSON dictionary,
    and prepares ID and name columns for mapping operations.

    Args:
        file_path: Path to the GeoJSON file to load.
        name_column: Column name containing district names. Defaults to "nazev_1".

    Returns:
        tuple: Contains 3 elements:
            - pd.DataFrame: Loaded and prepared DataFrame with 'id' and 'name' columns
            - GeoSeries: Centroid geometries for label placement
            - dict: GeoJSON dictionary for Plotly choropleth layer

    Examples:
        >>> from src.configs.data_config import DATA_PATHS
        >>> df, centroids, geojson = load_and_prepare_data(
        ...     DATA_PATHS.prague_districts,
        ...     "nazev_1"
        ... )
        >>> print(df.columns)
        Index(['id', 'name', ...])
    """
    df = read_file(file_path)
    df[name_column] = df[name_column].fillna("Unknown").astype(str).str.strip()
    centroids = compute_centroids(df, projected_epsg=5514)
    geojson = geodata_to_geojson_dict(df)

    df["id"] = df.index
    df["name"] = df[name_column]

    return df, centroids, geojson


class DistrictMapBuilder:
    """Builder for creating interactive Prague district maps with multiple layers.

    Provides a fluent interface for constructing Plotly maps of Prague districts.
    Supports choropleth base layers, text labels, scatter points, and polygon
    overlays. Handles styling, interaction modes, and layer composition.

    Attributes:
        style: Map style configuration object.
        layout: Map layout configuration object.
        layer_builder: MapLayerBuilder instance for creating map layers.
        click_mode: Plotly click interaction mode.
        drag_mode: Plotly drag interaction mode.
        selection_revision: Whether to update selection on data changes.
        choropleth_hover_info: Hover template for choropleth layer.
        custom_traces: List of additional Plotly traces to add to map.

    Examples:
        >>> from src.components.graphs.maps.districts import DistrictMapBuilder
        >>> from src.configs.data_config import DATA_PATHS
        >>>
        >>> # Create basic map
        >>> builder = DistrictMapBuilder(style=style_config, layout=layout_config)
        >>> df, centroids, geojson = load_and_prepare_data(DATA_PATHS.prague_districts)
        >>> fig = builder.create_map(df, centroids, geojson)
        >>>
        >>> # Add scatter points using fluent interface
        >>> fig = (builder
        ...     .add_scatter_points(parking_data, marker_color='blue')
        ...     .add_scatter_points(metro_data, marker_color='red')
        ...     .create_map(df, centroids, geojson))
    """

    def __init__(self, style = None, layout = None, click_mode: str = None, drag_mode: str = None, selection_revision: bool = False, choropleth_hover_info: str = None):
        """Initialize the DistrictMapBuilder with configuration.

        Args:
            style: Map style configuration object with color and appearance settings.
            layout: Map layout configuration object with zoom, height, and margins.
            click_mode: Plotly click interaction mode (e.g., 'event', 'select').
            drag_mode: Plotly drag interaction mode (e.g., 'zoom', 'pan').
            selection_revision: Whether to update selection on data changes. Defaults to False.
            choropleth_hover_info: Custom hover template for choropleth layer. Defaults to None.

        Examples:
            >>> builder = DistrictMapBuilder(
            ...     style=MAP_STYLE,
            ...     layout=MAP_LAYOUT,
            ...     click_mode='event'
            ... )
        """
        self.style = style
        self.layout = layout
        self.layer_builder = MapLayerBuilder(self.style)
        self.click_mode = click_mode
        self.drag_mode = drag_mode
        self.selection_revision=selection_revision,
        self.choropleth_hover_info = choropleth_hover_info
        self.custom_traces = []

        self.df = None
        self.centroids = None
        self.geojson = None

    def create_map(self, df: pd.DataFrame, centroids, geojson: dict, showlegend = True) -> go.Figure:
        """Create the complete Plotly map figure with all configured layers.

        Builds the final map by combining the choropleth base layer, text labels,
        highlight layer, and any custom traces (scatter points, polygons) that
        were added via fluent interface methods.

        Args:
            df: DataFrame containing district data with 'id' and 'name' columns.
            centroids: GeoSeries of centroid geometries for label placement.
            geojson: GeoJSON dictionary for the choropleth layer.
            showlegend: Whether to show the legend. Defaults to True.

        Returns:
            go.Figure: Complete Plotly Figure object ready for display.

        Examples:
            >>> builder = DistrictMapBuilder(style=style, layout=layout)
            >>> df, centroids, geojson = load_and_prepare_data(DATA_PATHS.prague_districts)
            >>> fig = builder.create_map(df, centroids, geojson)
        """
        fig = go.Figure()

        fig.add_trace(self.layer_builder.create_choropleth_layer(geojson, df, self.choropleth_hover_info))
        fig.add_trace(self.layer_builder.create_text_layer(centroids, df["name"]))
        fig.add_trace(self.layer_builder.create_highlight_layer())

        for trace in self.custom_traces:
            fig.add_trace(trace)

        center = calculate_center(df)
        fig.update_layout(
            map=dict(style=self.layout.style, center=center, zoom=self.layout.zoom),
            height=self.layout.height,
            margin=self.layout.margin,
            clickmode=self.click_mode,
            dragmode=self.drag_mode,
            showlegend=showlegend,
            selectionrevision=self.selection_revision,
        )

        return fig

    def add_scatter_points(
            self,
            data,
            lon_column: str = "geometry",
            lat_column: str = "geometry",
            hover_text_column: str = "hover_text",
            marker_size: int = 9,
            marker_color: str = "blue",
            marker_opacity: float = 0.8,
            show_legend: bool = False,
            legend_group: str = None,
            name: str = None,
    ):
        """Add scatter point layer to the map (fluent interface).

        Adds a scatter map layer showing point locations (e.g., parking meters,
        metro stations). Supports customization of marker appearance and hover text.
        Returns self for method chaining.

        Args:
            data: DataFrame or GeoDataFrame containing point data.
            lon_column: Column name for longitude values. Defaults to "geometry".
            lat_column: Column name for latitude values. Defaults to "geometry".
            hover_text_column: Column containing hover text. Defaults to "hover_text".
            marker_size: Size of markers in pixels. Defaults to 9.
            marker_color: Color for markers (CSS color or hex). Defaults to "blue".
            marker_opacity: Opacity of markers (0-1). Defaults to 0.8.
            show_legend: Whether to show this layer in legend. Defaults to False.
            legend_group: Group name for legend organization. Defaults to None.
            name: Display name for this layer. Defaults to None.

        Returns:
            DistrictMapBuilder: Self for method chaining.

        Examples:
            >>> builder.add_scatter_points(
            ...     parking_data,
            ...     marker_color='#3b82f6',
            ...     marker_size=8,
            ...     name='Parking Meters'
            ... ).add_scatter_points(
            ...     metro_data,
            ...     marker_color='#ef4444',
            ...     name='Metro Stations'
            ... )
        """
        trace = self.layer_builder.create_scatter_layer(
            data=data,
            lon_column=lon_column,
            lat_column=lat_column,
            hover_text_column=hover_text_column,
            marker_size=marker_size,
            marker_color=marker_color,
            marker_opacity=marker_opacity,
            show_legend=show_legend,
            legend_group=legend_group,
            name=name,
        )
        self.custom_traces.append(trace)
        return self

    def add_polygon_layer(
            self,
            geojson: Dict,
            df: pd.DataFrame,
            background_color: str = None,
            legend_group: str = None,
            name: str = None,
    ):
        """Add polygon overlay layer to the map (fluent interface).

        Adds a choropleth polygon layer showing areas (e.g., parking zones,
        no-standing areas). Supports custom background colors and legend grouping.
        Returns self for method chaining.

        Args:
            geojson: GeoJSON dictionary containing polygon geometries.
            df: DataFrame with data for the polygons, must have 'id' column
                matching GeoJSON feature IDs.
            background_color: Fill color for polygons (CSS color or hex).
                Defaults to None (uses default styling).
            legend_group: Group name for legend organization. Defaults to None.
            name: Display name for this layer in the legend. Defaults to None.

        Returns:
            DistrictMapBuilder: Self for method chaining.

        Examples:
            >>> builder.add_polygon_layer(
            ...     parking_zones_geojson,
            ...     parking_zones_df,
            ...     background_color='rgba(255, 0, 0, 0.3)',
            ...     name='Paid Parking Zones'
            ... )
        """
        trace = self.layer_builder.create_polygon_layer(
            geojson,
            df,
            background_color=background_color,
            legend_group=legend_group,
            name=name,
        )
        self.custom_traces.append(trace)
        return self


