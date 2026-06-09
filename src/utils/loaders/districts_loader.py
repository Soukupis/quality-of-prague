from src.configs.data_config import DATA_PATHS
from src.utils.loaders.data_loader import read_file

def get_districts_data():
    """Load Prague districts (mestske casti) geographic data.

    Returns:
        GeoDataFrame: Districts of Prague with administrative boundaries
            and metadata.

    Examples:
        >>> districts = get_districts_data()
        >>> print(f"Prague has {len(districts)} districts")
    """
    return read_file(DATA_PATHS.prague_districts)

def get_police_stations_data():
    """Load municipal police stations location data.

    Returns:
        GeoDataFrame: Point locations of police stations (objekty mestske
            policie) in Prague.

    Examples:
        >>> stations = get_police_stations_data()
        >>> print(f"Found {len(stations)} police stations")
    """
    return read_file(DATA_PATHS.police_stations)

def get_parking_meters_data():
    """Load parking meter location data.

    Returns:
        GeoDataFrame: Point locations of parking meters (parkovaci automaty)
            throughout Prague.

    Examples:
        >>> meters = get_parking_meters_data()
        >>> print(f"Total parking meters: {len(meters)}")
    """
    return read_file(DATA_PATHS.parking_meters)

def get_no_standing_data():
    """Load no-standing zones data.

    Returns:
        GeoDataFrame: Areas where stopping/standing is prohibited (zakaz stani)
            in Prague.

    Examples:
        >>> zones = get_no_standing_data()
        >>> print(f"No-standing zones: {len(zones)}")
    """
    return read_file(DATA_PATHS.no_standing)

def get_loading_zone_data():
    """Load loading zone location data.

    Returns:
        GeoDataFrame: Designated loading zones (vyhrazene stani pro zasobovani)
            for commercial deliveries.

    Examples:
        >>> zones = get_loading_zone_data()
        >>> print(f"Loading zones: {len(zones)}")
    """
    return read_file(DATA_PATHS.loading_zone)

def get_designated_parking_data():
    """Load special designated parking area data.

    Returns:
        GeoDataFrame: Special designated parking areas (vyhrazene stani
            specialni) in Prague.

    Examples:
        >>> parking = get_designated_parking_data()
        >>> print(f"Designated parking areas: {len(parking)}")
    """
    return read_file(DATA_PATHS.designated_parking)

def get_paid_parking_data():
    """Load paid parking zone data.

    Returns:
        GeoDataFrame: Paid parking zones (useky placeneho stani) where
            parking fees apply.

    Examples:
        >>> zones = get_paid_parking_data()
        >>> print(f"Paid parking zones: {len(zones)}")
    """
    return read_file(DATA_PATHS.paid_parking)

def get_ztp_parking_data():
    """Load disabled parking spaces data.

    Returns:
        GeoDataFrame: Parking spaces designated for disabled persons
            (parkovaci stani ZTP) in Prague.

    Examples:
        >>> spaces = get_ztp_parking_data()
        >>> print(f"Disabled parking spaces: {len(spaces)}")
    """
    return read_file(DATA_PATHS.ztp_parking)

def get_parking_p_r_data():
    """Load Park and Ride facility data.

    Returns:
        GeoDataFrame: Park and Ride (P+R) facilities for public transport
            users in Prague.

    Examples:
        >>> facilities = get_parking_p_r_data()
        >>> print(f"P+R facilities: {len(facilities)}")
    """
    return read_file(DATA_PATHS.parking_p_r)

def get_subway_entrances_data():
    """Load metro station entrance location data.

    Returns:
        GeoDataFrame: Point locations of metro/subway entrances (vstupy do metra)
            throughout Prague.

    Examples:
        >>> entrances = get_subway_entrances_data()
        >>> print(f"Metro entrances: {len(entrances)}")
    """
    return read_file(DATA_PATHS.subway_entrances)


def get_parks_data():
    """Load Prague parks and green spaces data (OpenStreetMap).

    Returns:
        GeoDataFrame: Centroid points of parks (leisure=park) within Prague bbox.
    """
    return read_file(DATA_PATHS.parks)


def get_nextbike_data():
    """Load Nextbike Prague bike-sharing station data (GBFS v2.3).

    Returns:
        GeoDataFrame: Point locations of Nextbike stations in Prague.
    """
    return read_file(DATA_PATHS.nextbike)


def get_pid_stops_data():
    """Load PID (Prague Integrated Transport) public transport stop data.

    Returns:
        GeoDataFrame: Point locations of all PID stop platforms in Prague.
    """
    return read_file(DATA_PATHS.pid_stops)


def get_chmi_stations_data():
    """Load ČHMÚ air quality monitoring station locations.

    Returns:
        GeoDataFrame: Point locations of ČHMÚ stations monitoring air quality in Prague.
    """
    return read_file(DATA_PATHS.chmi_stations)