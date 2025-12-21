"""District map styling and layout configuration dataclasses.

This module provides configuration dataclasses for styling and laying out
Prague district maps. Includes settings for colors, borders, zoom levels,
and map dimensions for both full city and single district views.

Classes:
    DistrictMapStyle: Visual styling configuration for district maps
    DistrictMapLayout: Layout configuration for full Prague map
    SingleDistrictMapLayout: Layout configuration for single district map
"""
from dataclasses import dataclass

@dataclass
class DistrictMapStyle:
    """Visual styling configuration for district maps.

    Defines colors, borders, and text styling for district map visualizations.
    Used for choropleth layers, borders, labels, and highlights.

    Attributes:
        background_color: Fill color for district polygons. Defaults to "#6BA6F0" (blue).
        border_color: Color for district borders. Defaults to "#DDDDDD" (light gray).
        border_width: Width of district borders in pixels. Defaults to 1.
        text_color: Color for district name labels. Defaults to "black".
        text_size: Font size for district labels in points. Defaults to 12.
        highlight_color: Color for highlighting selected districts. Defaults to "black".
        highlight_width: Width of highlight borders in pixels. Defaults to 3.

    Examples:
        >>> style = DistrictMapStyle()
        >>> style.background_color = "#FF0000"  # Change to red
        >>>
        >>> # Use in map builder
        >>> builder = DistrictMapBuilder(style=DistrictMapStyle())
    """
    background_color = "#6BA6F0"
    border_color = "#DDDDDD"
    border_width = 1
    text_color = "black"
    text_size = 12
    highlight_color = "black"
    highlight_width = 3


@dataclass
class DistrictMapLayout:
    """Layout configuration for full Prague district map.

    Defines the map style, zoom level, dimensions, and margins for the
    complete Prague city view showing all districts. Used on the districts
    overview page.

    Attributes:
        style: Plotly map style name. Defaults to "white-bg".
        zoom: Initial zoom level for the map. Defaults to 10.5 (city view).
        height: Map height in pixels. Defaults to 900.
        margin: Plot margins as dict with l, r, t, b keys. Defaults to all zeros.

    Examples:
        >>> layout = DistrictMapLayout()
        >>> layout.zoom = 11  # Zoom in closer
        >>>
        >>> # Use in map creation
        >>> builder = DistrictMapBuilder(layout=DistrictMapLayout())
    """
    style = "white-bg"
    zoom = 10.5
    height = 900
    margin = None

    def __post_init__(self):
        """Initialize margin to zero if not provided."""
        if self.margin is None:
            self.margin = dict(l=0, r=0, t=0, b=0)


@dataclass
class SingleDistrictMapLayout:
    """Layout configuration for single district focused map.

    Defines the map style, zoom level, dimensions, and margins for a
    detailed view of one specific district. Used on district detail pages
    with closer zoom for better visibility of features.

    Attributes:
        style: Plotly map style name. Defaults to "carto-positron" (light theme).
        zoom: Initial zoom level for the map. Defaults to 12 (closer view).
        height: Map height in pixels. Defaults to 600.
        margin: Plot margins as dict with l, r, t, b keys. Defaults to all zeros.

    Examples:
        >>> layout = SingleDistrictMapLayout()
        >>> layout.height = 700  # Taller map
        >>>
        >>> # Use in single district map
        >>> builder = DistrictMapBuilder(layout=SingleDistrictMapLayout())
    """
    style = "carto-positron"
    zoom = 12
    height = 600
    margin = None

    def __post_init__(self):
        """Initialize margin to zero if not provided."""
        if self.margin is None:
            self.margin = dict(l=0, r=0, t=0, b=0)