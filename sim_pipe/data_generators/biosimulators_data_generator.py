from typing import Dict
import zarr
from biosimulators_utils.config import Config


class BiosimulatorsDataGenerator:
    def __init__(self, archive_fp: str, output_dir: str, config: Config):
        raise NotImplementedError

    def get_result(self) -> Dict:
        raise NotImplementedError

    def to_zarr(self) -> zarr.Array:
        raise NotImplementedError

