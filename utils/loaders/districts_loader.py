from data_config import DATA_PATHS
from utils.loaders.data_loader import read_file

def get_districts_data():
    return read_file(DATA_PATHS.prague_districts)

def get_police_stations_data():
    return read_file(DATA_PATHS.police_stations)

def get_parking_meters_data():
    return read_file(DATA_PATHS.parking_meters)