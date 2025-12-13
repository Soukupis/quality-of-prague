from src.components.ui import info_card, section_header, info_card_row
from src.configs.dataset_config import DATASET_CONFIGS
from src.utils.geospatial_utils import point_count_for_polygon
from src.utils.loaders.districts_loader import get_parking_meters_data, get_subway_entrances_data, \
    get_parking_p_r_data, get_no_standing_data
import dash_bootstrap_components as dbc
from src.components.config import theme


def travel_section(district, polygons):
    df = {
        "parking_meters": get_parking_meters_data(),
        "subway_entrances": get_subway_entrances_data(),
        "parking_p_r": get_parking_p_r_data(),
        "no_standing": get_no_standing_data(),
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
                    dataset_key=dataset_key
                )
            )

    if not cards:
        return None

    return dbc.Row([
        dbc.Col([
            section_header(
                title="Cestování",
                accent_color=theme.TRAVEL_ACCENT_COLOR,
                bg_color=theme.TRAVEL_BG_COLOR,
                text_color=theme.TRAVEL_TEXT_COLOR
            ),
            info_card_row(cards, col_width=4)
        ], width=12)
    ])