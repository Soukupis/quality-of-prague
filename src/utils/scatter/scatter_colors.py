"""Color configurations for scatter map layers.

This module defines color schemes for visualizing Prague metro/subway lines
on maps. Each metro line (A, B, C) has a distinct color, with different
opacity levels for points (stations) and circles (transfer zones).

Constants:
    SUBWAY_ENTRANCES_LINE_COLORS: Base colors for each metro line
    subway_entrances_color_to_rgba_points: Opaque RGBA colors for station points
    subway_entrances_color_to_rgba_circles: Semi-transparent RGBA for transfer circles

Color Scheme:
    - Line A: Green (rgba(0, 128, 0))
    - Line B: Gold/Yellow (rgba(245, 230, 83))
    - Line C: Red (rgba(255, 0, 0))

Examples:
    >>> from src.utils.scatter.scatter_colors import SUBWAY_ENTRANCES_LINE_COLORS
    >>> print(SUBWAY_ENTRANCES_LINE_COLORS['A'])
    'green'
    >>>
    >>> # Get RGBA color for station point
    >>> from src.utils.scatter.scatter_colors import subway_entrances_color_to_rgba_points
    >>> color = subway_entrances_color_to_rgba_points['green']
    >>> print(color)  # 'rgba(0, 128, 0, 0.9)'
"""
SUBWAY_ENTRANCES_LINE_COLORS = {
    "A": "green",
    "B": "gold",
    "C": "red"
}

# For transfer station points (opaque)
subway_entrances_color_to_rgba_points = {
    "green": "rgba(0, 128, 0, 0.9)",
    "gold": "rgba(245, 230, 83, 0.9)",
    "red": "rgba(255, 0, 0, 0.9)",
}
# For large circles (semi-transparent)
subway_entrances_color_to_rgba_circles = {
    "green": "rgba(0, 128, 0, 0.2)",
    "gold": "rgba(245, 230, 83, 0.2)",
    "red": "rgba(255, 0, 0, 0.2)",
}