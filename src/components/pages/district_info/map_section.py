"""Map section component for district detail pages.

This module provides the map visualization section shown on district detail pages,
displaying an interactive Plotly map of a single district with optional scatter
and polygon layers.
"""
from dash import html, dcc
from src.components.graphs import create_single_district_map


def map_section(district: str = None, scatters = None, polygons = None) -> html.Div:
    """Create the map section component for district detail page.

    Builds a Dash component containing an interactive Plotly map focused on
    a single Prague district. The map can display optional scatter point layers
    (e.g., parking meters, metro stations) and polygon layers (e.g., parking zones).

    Args:
        district: Name of the district to display (e.g., "Praha 1").
            Defaults to None.
        scatters: Dictionary of scatter layer configurations for point data.
            Keys are layer identifiers, values are config dicts with data
            and styling. Defaults to None.
        polygons: Dictionary of polygon layer configurations for area data.
            Keys are layer identifiers, values are config dicts with GeoJSON
            and styling. Defaults to None.

    Returns:
        html.Div: Dash Div component containing the dcc.Graph with the
            district map.

    Examples:
        >>> # Simple map without layers
        >>> section = map_section(district="Praha 1")
        >>>
        >>> # Map with scatter layers
        >>> scatter_config = {
        ...     'parking_meters': {
        ...         'data': parking_df,
        ...         'marker_color': 'blue'
        ...     }
        ... }
        >>> section = map_section("Praha 1", scatters=scatter_config)
    """
    return html.Div([
        dcc.Graph(
            id="single-district-map",
            figure=create_single_district_map(district, scatters, polygons),
            config={
                'displayModeBar': False,
            },
            style={"marginBottom": "60px", "width": "100%"}
        )
    ], style={"width": "100%"})