from dataclasses import dataclass
from pathlib import Path
from typing import Dict

@dataclass
class DataPaths:
    base_data_dir = Path("data")

    prague_districts = base_data_dir / "mestske_casti" / "mestske_casti.geojson"

    def get_path(self, path_key: str) -> str:
        return str(getattr(self, path_key))

DATA_PATHS = DataPaths()