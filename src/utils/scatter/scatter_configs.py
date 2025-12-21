"""Scatter layer visualization configurations.

This module defines styling and display configurations for point-based map
layers in the application. Each scatter layer has specific marker properties,
colors, and legend settings for consistent visualization across the app.

Constants:
    SCATTER_LAYER_CONFIGS: Dictionary mapping layer keys to their visualization
        configurations. Each config includes:
        - marker_size: Size of marker points in pixels
        - marker_color: Hex color code for markers
        - marker_opacity: Opacity value (0-1)
        - name: Display name in Czech for legend
        - legend_group: Category for legend organization

Configured Layers:
    - parking_meters: Purple markers for parking meters
    - parking_p_r: Green markers for Park & Ride facilities
    - police_stations: Blue markers for police stations
    - ztp_parking: Orange markers for disabled parking spaces

Examples:
    >>> from src.utils.scatter.scatter_configs import SCATTER_LAYER_CONFIGS
    >>> config = SCATTER_LAYER_CONFIGS['parking_meters']
    >>> print(config['marker_color'])
    '#8B008B'
    >>> print(config['name'])
    'Parkovací automaty'
    >>>
    >>> # Use in scatter builder
    >>> for layer_key, config in SCATTER_LAYER_CONFIGS.items():
    ...     marker_color = config['marker_color']
    ...     marker_size = config['marker_size']
"""
SCATTER_LAYER_CONFIGS = {
    "parking_meters": {
        "marker_size": 10,
        "marker_color": "#8B008B",
        "marker_opacity": 1,
        "name": "Parkovací automaty",
        "legend_group": "Doprava",
    },
    "parking_p_r": {
        "marker_size": 10,
        "marker_color": "#2E7D32",
        "marker_opacity": 1,
        "name": "Parkoviště P+R",
        "legend_group": "Doprava",
    },
    "police_stations": {
        "marker_size": 10,
        "marker_color": "#1565C0",
        "marker_opacity": 1,
        "name": "Policejní stanice",
        "legend_group": "Bezpečnost",
    },
    "ztp_parking": {
        "marker_size": 10,
        "marker_color": "#F57C00",
        "marker_opacity": 1,
        "name": "Parkovací stání ZTP",
        "legend_group": "Doprava",
    }
}
