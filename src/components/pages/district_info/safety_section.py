"""Safety metrics section component for district detail pages.

This module provides the safety section showing security-related metrics
for a district, such as the number of police stations within the district
boundaries.
"""
from src.components.ui import info_card, section_header
from src.configs.dataset_config import DATASET_CONFIGS
from src.utils.geospatial_utils import point_count_for_polygon
from src.utils.loaders.districts_loader import get_police_stations_data
import dash_bootstrap_components as dbc
from src.components.config import theme


def safety_section(district, polygons):
    """Create the safety metrics section for a district detail page.

    Builds a section displaying safety-related statistics for a specific Prague
    district. Currently shows the count of police stations within the district
    boundaries. Info cards are interactive and can toggle map layers.

    Args:
        district: Name of the district (e.g., "Praha 1").
        polygons: Dictionary mapping district names to their Shapely polygon
            geometries. Used for spatial filtering of police stations.

    Returns:
        dbc.Row: Bootstrap Row component containing the safety section with
            header and info cards. Returns None if no safety datasets are
            configured.

    Examples:
        >>> from src.utils.districts.district_utils import get_district_polygons
        >>> polygons = get_district_polygons()
        >>> section = safety_section("Praha 1", polygons)
        >>> # section contains police station count card
    """
    police_stations = get_police_stations_data()

    cards = []
    for dataset_key, config in DATASET_CONFIGS.items():
        if config.get("section") == "safety":
            if dataset_key == "police_stations":
                data = police_stations
                count = point_count_for_polygon(polygons[district], data, "geometry")
                cards.append(
                    info_card(
                        config["icon"],
                        config["title"],
                        count,
                        "info",
                        card_id=config["id"],
                        dataset_key=dataset_key,
                        compact=True
                    )
                )

    if not cards:
        return None

    return dbc.Row([
        dbc.Col([
            section_header(
                title="Bezpečnost",
                accent_color=theme.SAFETY_ACCENT_COLOR,
                bg_color=theme.SAFETY_BG_COLOR,
                text_color=theme.SAFETY_TEXT_COLOR
            ),
            dbc.Row([dbc.Col(card, xs=6, sm=4, md=3, className="mb-3") for card in cards], className="g-2 mb-2")
        ], width=12)
    ])