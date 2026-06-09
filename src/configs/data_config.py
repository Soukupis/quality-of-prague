from dataclasses import dataclass

@dataclass(frozen=True)
class DataPaths:
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
    parks: str = "parky_praha/parky_praha.geojson"
    nextbike: str = "nextbike_stanice/nextbike_stanice.geojson"
    pid_stops: str = "zastavky_pid/zastavky_pid.geojson"
    chmi_stations: str = "stanice_kvality_ovzdusi/stanice_kvality_ovzdusi.geojson"

    def get_path(self, path_key: str) -> str:
        return getattr(self, path_key)

    def get_dataset_value_options(self):
        label_map = {
            'police_stations': 'Policejní stanice',
            'parking_meters': 'Parkovací automaty',
            'subway_entrances': 'Vstupy do metra',
            'no_standing': 'Zákaz stání',
            'parking_p_r': 'Parkoviště P+R',
            'loading_zone': 'Zásobování',
            'designated_parking': 'Stání speciální',
            'paid_parking': 'Placené stání',
            'ztp_parking': 'Parkovací stání ZTP',
            'parks': 'Parky a zeleň',
            'nextbike': 'Nextbike stanice',
            'pid_stops': 'Zastávky PID',
        }

        return [
            {'label': label_map[field], 'value': field}
            for field in label_map.keys()
        ]

DATA_PATHS = DataPaths()