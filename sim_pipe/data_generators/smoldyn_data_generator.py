import os
from enum import Enum
from typing import Optional, Tuple, Dict, List
from smoldyn import Simulation
import smoldyn
import numpy as np
import pandas as pd
import zarr
from smoldyn import biosimulators as bioSim
from simulariumio.smoldyn.smoldyn_data import InputFileData, SmoldynData
from smoldyn.biosimulators.data_model import SmoldynOutputFile
from biosimulators_utils.config import Config, get_config
from biosimulators_utils.sedml.data_model import Task, Model, ModelLanguage
from simulariumio.smoldyn import SmoldynConverter, SmoldynData
from simulariumio.filters import TranslateFilter
from simulariumio import (
    TrajectoryData,
    CameraData,
    TrajectoryConverter,
    AgentData,
    UnitData,
    MetaData,
    DisplayData,
    DISPLAY_TYPE,
    ModelMetaData,
    BinaryWriter,
    InputFileData,
)
from biosimulators_utils.report.io import ReportFormat


class SmoldynDataGenerator:
    def __init__(self,
                 output_dirpath: str,
                 config: Optional[Config] = None):
        self.output_dirpath = output_dirpath
        self.config = config or get_config()
        self.config.LOG_PATH = self.output_dirpath
        self.config.REPORT_FORMATS = [ReportFormat.csv]

    @staticmethod
    def run_simulation_from_smoldyn_file(model_fp: str) -> None:
        simulator = bioSim.combine.init_smoldyn_simulation_from_configuration_file(model_fp)
        return simulator.runSim()

    def run_simulation_from_archive(self, archive_fp: str) -> Tuple:
        return bioSim.exec_sedml_docs_in_combine_archive(
            archive_filename=archive_fp,
            out_dir=self.output_dirpath,
            config=self.config
        )

    def run_simulation_from_sed_doc(self, archive_dirpath: str) -> Tuple:
        for root, _, files in os.walk(archive_dirpath):
            for f in files:
                fp = os.path.join(root, f)
                if fp.endswith('.sedml'):
                    return bioSim.exec_sed_doc(
                        doc=fp,
                        working_dir=archive_dirpath,
                        base_out_path=self.output_dirpath,
                        config=self.config
                    )

    @staticmethod
    def prepare_simularium_fp(simularium_dirpath: str, simularium_fname: str) -> str:
        if not os.path.exists(simularium_dirpath):
            os.mkdir(simularium_dirpath)
        return os.path.join(simularium_dirpath, simularium_fname)

    @staticmethod
    def prepare_input_file_data(output_filepath: str) -> InputFileData:
        return InputFileData(output_filepath)

    @staticmethod
    def prepare_smoldyn_data_for_conversion(
            file_data: InputFileData,
            spatial_units="nm",
            temporal_units="ns"
    ) -> SmoldynData:
        return SmoldynData(
            smoldyn_file=file_data,
            spatial_units=UnitData(spatial_units),
            time_units=UnitData(temporal_units),
        )

    @staticmethod
    def translate_data(data: SmoldynData, box_size: float, n_dim=3):
        c = SmoldynConverter(data)
        translation_magnitude = -box_size / 2
        return c.filter_data([
            TranslateFilter(
                translation_per_type={},
                default_translation=translation_magnitude * np.ones(n_dim)
            ),
        ])

    @staticmethod
    def convert_to_simularium(data, simularium_filename: str):
        BinaryWriter.save(
            data,
            simularium_filename,
            validate_ids=False
        )

    def generate_simularium_file(
            self,
            file_data_path: str,
            simularium_filename: str,
            box_size: float,
            n_dim=3
            ):
        input_file = self.prepare_input_file_data(file_data_path)
        data = self.prepare_smoldyn_data_for_conversion(input_file)
        translated = self.translate_data(data, box_size, n_dim)
        self.convert_to_simularium(translated, simularium_filename)
        print('New Simularium file generated!!')

    @staticmethod
    def prepare_agent_data():
        pass

    @staticmethod
    def generate_display_data_object(
            name: str,
            radius: float,
            display_type=DISPLAY_TYPE.OBJ
            ) -> DisplayData:
        return DisplayData(
                    name=name,
                    radius=radius,
                    display_type=display_type
                    )

    def generate_display_data_object_dict(self, agent_names: List[Tuple[str, str, float]]) -> Dict[str, DisplayData]:
        """
        Params:
        -------
        agent_names: `List[Tuple[str, str, float]]` -> a list of tuples defining the Display Data configuration parameters.\n
        The Tuple is expected to be as such: [(`agent_name: str`, `display_name: str`, `radius: float`)]

        """
        data = {}
        for name in agent_names:
            data[name[0]] = self.generate_display_data_object(name[1], name[2])
        return data


class SimulationSetup(str, Enum):
    project_root = 'sim_pipe'
    model_fp = 'sim_pipe/files/models/ecoli_model.txt'
    ecoli_archive_dirpath = 'sim_pipe/files/archives/Andrews_ecoli_0523'
    sed_doc = os.path.join(ecoli_archive_dirpath, 'simulation.sedml')
    outputs_dirpath = 'sim_pipe/outputs'

