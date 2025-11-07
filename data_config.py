from dataclasses import dataclass
from pathlib import Path
from typing import Dict

@dataclass(frozen=True)
class DataPaths:
    base_data_dir = Path("data")

    prague_districts = base_data_dir / "mestske_casti" / "mestske_casti.geojson"
    police_stations = base_data_dir / "objekty_mestske_policie_praha" / "objekty_mestske_policie_praha.geojson"
    parking_meters = base_data_dir / "parkovaci_automaty" / "parkovaci_automaty.geojson"


    def get_path(self, path_key: str) -> str:
        return str(getattr(self, path_key))

DATA_PATHS = DataPaths()