"""Prague district map creation functions.

This module provides high-level functions for creating interactive Plotly maps
of Prague districts. Supports both full city views and single-district focused
maps with optional data layers (scatter points and polygons).
"""
import plotly.graph_objects as go
from .district_map_builder import DistrictMapBuilder, load_and_prepare_data
from src.configs.data_config import DATA_PATHS
from .district_map_config import SingleDistrictMapLayout, DistrictMapStyle,DistrictMapLayout
from src.utils.scatter.scatter_utils import build_subway_entrance_traces

def get_single_district_map_builder(district: str) -> DistrictMapBuilder:
    """Create and configure a map builder for a single district.

    Loads district data and filters it to just the specified district, creating
    a configured DistrictMapBuilder ready for adding layers and generating
    the final map figure.

    Args:
        district: Name of the district (e.g., "Praha 1", "Praha 2").

    Returns:
        DistrictMapBuilder: Configured builder instance with filtered district
            data, centroids, and GeoJSON ready for map creation.

    Examples:
        >>> builder = get_single_district_map_builder("Praha 1")
        >>> fig = builder.create_map(builder.df, builder.centroids, builder.geojson)
    """
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
    """Create an interactive map of all Prague districts.

    Builds a complete choropleth map showing all Prague districts with
    interactive selection capabilities. Used on the districts overview page.

    Returns:
        go.Figure: Plotly Figure object with all Prague districts displayed,
            configured for click events and selection mode.

    Examples:
        >>> fig = create_prague_map()
        >>> # fig is ready to display in dcc.Graph component
        >>> # Clicking districts triggers navigation to district detail
    """
    builder = DistrictMapBuilder(DistrictMapStyle(), DistrictMapLayout(), "event+select", "select", True, "text")
    df, centroids, geojson = load_and_prepare_data(DATA_PATHS.get_path("prague_districts"))
    return builder.create_map(df, centroids, geojson)

def create_single_district_map(district: str, scatters = None, polygons = None, showlegend: bool = True) -> go.Figure:
    """Create a focused map of a single district with optional data layers.

    Builds an interactive map centered on one specific Prague district. Can
    overlay scatter point layers (e.g., parking meters, metro stations) and
    polygon layers (e.g., parking zones). Handles special visualization for
    subway entrances with line-specific coloring.

    Args:
        district: Name of the district to display (e.g., "Praha 1").
        scatters: Dictionary of scatter layer configurations. Keys are layer
            identifiers, values are dicts with 'data', 'lon_column',
            'lat_column', 'marker_size', 'marker_color', 'marker_opacity',
            'legend_group', and 'name'. Special handling for type
            "subway_entrances". Defaults to None.
        polygons: Dictionary of polygon layer configurations. Keys are layer
            identifiers, values are dicts with GeoJSON and styling properties.
            Defaults to None.
        showlegend: Whether to show the legend. Defaults to True.

    Returns:
        go.Figure: Plotly Figure object showing the district map with all
            requested layers overlaid.

    Examples:
        >>> # Simple district map without layers
        >>> fig = create_single_district_map("Praha 1")
        >>>
        >>> # Map with parking meters layer
        >>> scatter_config = {
        ...     'parking_meters': {
        ...         'data': parking_df,
        ...         'lon_column': 'geometry',
        ...         'lat_column': 'geometry',
        ...         'marker_size': 8,
        ...         'marker_color': 'blue',
        ...         'marker_opacity': 0.8,
        ...         'legend_group': 'Doprava',
        ...         'name': 'Parkovací automaty'
        ...     }
        ... }
        >>> fig = create_single_district_map("Praha 1", scatters=scatter_config)
    """

    map_builder = get_single_district_map_builder(district)

    if scatters is not None:
        for scatter_key, scatter_config in scatters.items():
            if scatter_config.get("type") == "subway_entrances":
                # Handle subway entrances with special visualization
                subway_traces = build_subway_entrance_traces(scatter_config["data"])
                for trace in subway_traces:
                    map_builder.custom_traces.append(trace)
            else:
                # Handle regular scatter points
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




