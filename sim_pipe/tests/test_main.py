from sim_pipe.data_generators.smoldyn_data_generator import SmoldynDataGenerator, SmoldynDataConverter
from smoldyn import Simulation
from simulariumio import InputFileData, DisplayData
import os
from typing import Dict
from simulariumio.smoldyn import SmoldynConverter, SmoldynData

MODEL_FP = 'sim_pipe/files/models/ecoli_model.txt'
MODEL_OUTPUT_FP = 'sim_pipe/files/models/ecoli_modelout.txt'
ECOLI_ARCHIVE_DIRPATH = 'sim_pipe/files/archives/Andrews_ecoli_0523'
SED_DOC_PATH = os.path.join(ECOLI_ARCHIVE_DIRPATH, 'simulation.sedml')
SIMULARIUM_FILENAME = 'ecoli_spatial_3'

BOX_SIZE = 1.
N_DIM = 3
AGENTS = [
    ('MinD_ATP(front)', 'D_d', 2.0, "#FFFF00"),
    ('MinE(solution)', 'D_E', 1.0, "#800080"),
    ('MinD_ATP(solution)', 'SIGMA_D', 1.0, "#FF0000"),
    ('MinD_ADP(solution)', 'D_D', 1.0, "#008000"),
    ('MinDMinE(front)', 'D_de', 1.0, "#FFA500"),
]


def main():
    generator = SmoldynDataGenerator()
    converter = SmoldynDataConverter()

    sim = generate_simulation(generator)
    run_simulation(sim)


def generate_simulation(g: SmoldynDataGenerator) -> Simulation:
    return g.generate_simulation_object_from_configuration_file(MODEL_FP)


def run_simulation(s: Simulation) -> None:
    return s.runSim()


def prepare_simularium_dir(c: SmoldynDataConverter) -> str:
    return c.prepare_simularium_fp()


def generate_input_file_data(c: SmoldynDataConverter) -> InputFileData:
    return c.prepare_input_file_data(MODEL_OUTPUT_FP)


def generate_display_obj_dict(c: SmoldynDataConverter) -> Dict:
    return c.generate_display_data_object_dict(AGENTS)


def generate_smoldyn_data_object(
        c: SmoldynDataConverter,
        fd: InputFileData,
        dd: DisplayData
        ) -> SmoldynData:
    return c.prepare_smoldyn_data_for_conversion(
        file_data=fd,
        display_data=dd
    )
