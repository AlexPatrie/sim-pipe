from typing import Tuple, Dict, List, Optional
import os
import zarr
import pandas as pd
from smoldyn import biosimulators
from biosimulators_utils.config import Config, get_config
from sim_pipe.data_generators.biosimulators_data_generator import BiosimulatorsDataGenerator


class SmoldynDataGenerator(BiosimulatorsDataGenerator):
    def __init__(self, archive_fp: str, output_dir: str, config: Optional[Config] = None):
        """
        Run a biosimulators smoldyn simulation. Wraps `smoldyn.biosimulators.combine.exec`\n

        Params
        ______
        `archive_fp: str`: path to OMEX/COMBINE archive file\n
        `output_dir: str`: path to house simulation outputs\n
        `config: Config`: biosimulators common configuration
        """
        self.archive_fp = archive_fp
        self.output_dir = output_dir
        self.config = config or get_config()
        self.config.LOG_PATH = self.output_dir
        self.data = self.get_result()

    def get_result(self) -> Dict:
        results, log = biosimulators.exec_sedml_docs_in_combine_archive(
            archive_filename=self.archive_fp,
            out_dir=self.output_dir,
            config=self.config
        )
        return {'results': results, 'log': log}

    def to_zarr(self, chunks=(10, 10)) -> zarr.Array:
        data = self.data.get('results')
        return zarr.array(data, chunks=chunks)

    def get_result_dataframe(self) -> pd.DataFrame:
        csv_dir = os.path.join(self.output_dir, "simulation.sedml")
        for f in os.listdir(csv_dir):
            if f.endswith('.csv'):
                raw_df = pd.read_csv(os.path.join(csv_dir, f), header=None)
                cols = raw_df.pop(0).values.tolist()
                transposed_dataframe = raw_df.T
                return pd.DataFrame(data=transposed_dataframe.values, columns=cols)



