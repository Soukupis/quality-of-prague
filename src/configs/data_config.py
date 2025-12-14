from dataclasses import dataclass

@dataclass(frozen=True)
class DataPaths:
    """Data paths configuration for accessing geospatial data files.

    These paths are relative to the 'data' package and are used with
    importlib.resources for robust package resource access.
    """

    prague_districts: str = "mestske_casti/mestske_casti.geojson"
    police_stations: str = "objekty_mestske_policie_praha/objekty_mestske_policie_praha.geojson"
    parking_meters: str = "parkovaci_automaty/parkovaci_automaty.geojson"
    subway_entrances: str = "vstupy_do_metra/vstupy_do_metra.geojson"
    no_standing: str = "zakaz_stani/zakaz_stani.geojson"
    parking_p_r: str = "parkovani_p_r/parkovani_p_r.geojson"
    loading_zone: str = "vyhrazene_stani_pro_zasobovani/vyhrazene_stani_pro_zasobovani.geojson"
    designated_parking: str = "vyhrazene_stani_specialni/vyhrazene_stani_specialni.geojson"
    paid_parking: str = "useky_placeneho_stani/useky_placeneho_stani.geojson"
    ztp_parking: str = "parkovaci_stani_ztp/parkovaci_stani_ztp.geojson"

    def get_path(self, path_key: str) -> str:
        """Get a path as a string by key name."""
        return getattr(self, path_key)

DATA_PATHS = DataPaths()