"""
Central configuration for all datasets used in the district info page.
"""
from src.utils.loaders.districts_loader import get_parking_p_r_data, get_parking_meters_data, get_police_stations_data, \
    get_subway_entrances_data, get_no_standing_data, get_loading_zone_data, get_designated_parking_data, \
    get_paid_parking_data, get_ztp_parking_data

DATASET_CONFIGS = {
    "police_stations": {
        "id": "police-stations",
        "icon": "fa-building-shield",
        "title": "Police stations",
        "section": "safety",
        "layer_key": "police_stations",
        "loader_function": get_police_stations_data,
    },
    "parking_meters": {
        "id": "parking-meters",
        "icon": "fa-parking",
        "title": "Parkovací automaty",
        "section": "travel",
        "layer_key": "parking_meters",
        "loader_function": get_parking_meters_data,
    },
    "parking_p_r": {
        "id": "parking_p_r",
        "icon": "fa-car-side",
        "title": "Parkoviště P+R",
        "section": "travel",
        "layer_key": "parking_p_r",
        "loader_function": get_parking_p_r_data,
    },
    "no_standing": {
        "id": "no_standing",
        "icon": "fa-ban",
        "title": "Zákaz stání",
        "section": "travel",
        "layer_key": "no_standing",
        "loader_function": get_no_standing_data,
    },
    "loading_zone": {
        "id": "loading_zone",
        "icon": "fa-truck-ramp-box",
        "title": "Zásobování",
        "section": "travel",
        "layer_key": "loading_zone",
        "loader_function": get_loading_zone_data,
    },
    "designated_parking": {
        "id": "designated_parking",
        "icon": "fa-id-card",
        "title": "Stání speciální",
        "section": "travel",
        "layer_key": "designated_parking",
        "loader_function": get_designated_parking_data,
    },
    "paid_parking": {
        "id": "paid_parking",
        "icon": "fa-coins",
        "title": "Placené stání",
        "section": "travel",
        "layer_key": "paid_parking",
        "loader_function": get_paid_parking_data,
    },
    "subway_entrances": {
        "id": "subway_entrances",
        "icon": "fa-subway",
        "title": "Vstupy do metra",
        "section": "travel",
        "layer_key": "subway_entrances",
        "loader_function": get_subway_entrances_data,
    },
    "ztp_parking": {
        "id": "ztp_parking",
        "icon": "fa-wheelchair",
        "title": "Parkovací stání ZTP",
        "section": "travel",
        "layer_key": "ztp_parking",
        "loader_function": get_ztp_parking_data,
    }
}
