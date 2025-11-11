"""
Central configuration for all datasets used in the district info page.
"""
from utils.loaders.districts_loader import get_parking_meters_data, get_police_stations_data, get_subway_entrances_data

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
        "title": "Parking meters",
        "section": "travel",
        "layer_key": "parking_meters",
        "loader_function": get_parking_meters_data,
    },
    "subway_entrances": {
        "id": "subway_entrances",
        "icon": "fa-subway",
        "title": "Subway entrances",
        "section": "travel",
        "layer_key": "subway_entrances",
        "loader_function": get_subway_entrances_data,
    },
}
