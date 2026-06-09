"""Travel and transportation metrics section for district detail pages.

This module provides the transportation section showing mobility-related metrics
for a district, including parking facilities, metro stations, parking zones, and
other transportation infrastructure.
"""
from src.components.ui import info_card, section_header
from src.configs.dataset_config import DATASET_CONFIGS
from src.utils.geospatial_utils import point_count_for_polygon
from src.utils.loaders.districts_loader import get_parking_meters_data, get_subway_entrances_data, \
    get_parking_p_r_data, get_no_standing_data, get_loading_zone_data, get_designated_parking_data, \
    get_paid_parking_data, get_ztp_parking_data
import dash_bootstrap_components as dbc
from src.components.config import theme


def travel_section(district, polygons):
    """Create the transportation metrics section for a district detail page.

    Builds a section displaying transportation-related statistics for a specific
    Prague district. Shows counts of various facilities and zones within the
    district boundaries:
    - Parking meters
    - Metro/subway entrances
    - Park and Ride facilities
    - No-standing zones
    - Loading zones
    - Designated parking areas
    - Paid parking zones
    - Disabled (ZTP) parking spaces

    All info cards are interactive and can toggle corresponding map layers.

    Args:
        district: Name of the district (e.g., "Praha 1").
        polygons: Dictionary mapping district names to their Shapely polygon
            geometries. Used for spatial filtering of transportation features.

    Returns:
        dbc.Row: Bootstrap Row component containing the transportation section
            with header and info cards. Returns None if no travel datasets are
            configured.

    Examples:
        >>> from src.utils.districts.district_utils import get_district_polygons
        >>> polygons = get_district_polygons()
        >>> section = travel_section("Praha 1", polygons)
        >>> # section contains cards for all transportation metrics
    """
    df = {
        "parking_meters": get_parking_meters_data(),
        "subway_entrances": get_subway_entrances_data(),
        "parking_p_r": get_parking_p_r_data(),
        "no_standing": get_no_standing_data(),
        "loading_zone": get_loading_zone_data(),
        "designated_parking": get_designated_parking_data(),
        "paid_parking": get_paid_parking_data(),
        "ztp_parking": get_ztp_parking_data(),
    }

    cards = []
    for dataset_key, config in DATASET_CONFIGS.items():
        if config.get("section") == "travel":
            data = df[dataset_key]
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
                title="Doprava",
                accent_color=theme.TRAVEL_ACCENT_COLOR,
                bg_color=theme.TRAVEL_BG_COLOR,
                text_color=theme.TRAVEL_TEXT_COLOR
            ),
            dbc.Row([dbc.Col(card, xs=6, sm=4, md=3, className="mb-3") for card in cards], className="g-2 mb-2")
        ], width=12)
    ])