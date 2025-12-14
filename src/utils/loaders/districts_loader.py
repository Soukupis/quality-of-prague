from src.configs.data_config import DATA_PATHS
from src.utils.loaders.data_loader import read_file

def get_districts_data():
    return read_file(DATA_PATHS.prague_districts)

def get_police_stations_data():
    return read_file(DATA_PATHS.police_stations)

def get_parking_meters_data():
    return read_file(DATA_PATHS.parking_meters)

def get_no_standing_data():
    return read_file(DATA_PATHS.no_standing)

def get_loading_zone_data():
    return read_file(DATA_PATHS.loading_zone)

def get_designated_parking_data():
    return read_file(DATA_PATHS.designated_parking)

def get_paid_parking_data():
    return read_file(DATA_PATHS.paid_parking)

def get_ztp_parking_data():
    return read_file(DATA_PATHS.ztp_parking)

def get_parking_p_r_data():
    return read_file(DATA_PATHS.parking_p_r)

def get_subway_entrances_data():
    return read_file(DATA_PATHS.subway_entrances)