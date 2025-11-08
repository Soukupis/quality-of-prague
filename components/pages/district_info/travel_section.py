from components.ui import info_card, section_header, info_card_row
from dataset_config import DATASET_CONFIGS
from utils.geospatial_utils import point_count_for_polygon
from utils.loaders.districts_loader import get_parking_meters_data
import dash_bootstrap_components as dbc
from components.config import theme

def travel_section(district, polygons):
    parking_meters = get_parking_meters_data()

    cards = []
    for dataset_key, config in DATASET_CONFIGS.items():
        if config.get("section") == "travel":
            if dataset_key == "parking_meters":
                data = parking_meters
                count = point_count_for_polygon(polygons[district], data, "geometry")
                cards.append(
                    info_card(
                        config["icon"],
                        config["title"],
                        count,
                        "info",
                        card_id=config["id"],
                        dataset_key=dataset_key
                    )
                )

    if not cards:
        return None

    return dbc.Row([
        dbc.Col([
            section_header(
                title="Travel",
                accent_color=theme.TRAVEL_ACCENT_COLOR,
                bg_color=theme.TRAVEL_BG_COLOR,
                text_color=theme.TRAVEL_TEXT_COLOR
            ),
            info_card_row(cards, col_width=2)
        ], width=12)
    ])