import os
from smoldyn import Simulation
import smoldyn
import numpy as np
from smoldyn import biosimulators as bioSim
from simulariumio.smoldyn.smoldyn_data import InputFileData, SmoldynData
from smoldyn.biosimulators.data_model import SmoldynOutputFile
from biosimulators_utils.config import Config
from biosimulators_utils.sedml.data_model import Task, Model, ModelLanguage
from simulariumio.smoldyn import SmoldynConverter, SmoldynData
from simulariumio.filters import TranslateFilter
from simulariumio import (
    UnitData,
    MetaData,
    DisplayData,
    DISPLAY_TYPE,
    ModelMetaData,
    BinaryWriter,
    InputFileData,
)
from biosimulators_utils.report.io import ReportFormat

model_fp = 'sim_pipe/files/models/ecoli_model.txt'

ecoli_archive_dirpath = 'sim_pipe/files/archives/Andrews_ecoli_0523'
sed_doc = os.path.join(ecoli_archive_dirpath, 'simulation.sedml')
outputs_dirpath = 'sim_pipe/outputs'


def create_simulation_from_file() -> Simulation:
    return bioSim.combine.init_smoldyn_simulation_from_configuration_file(model_fp)


def run_simulation_from_sed_doc():
    sim_config = Config(LOG_PATH=outputs_dirpath, REPORT_FORMATS=[ReportFormat.csv])

    return bioSim.exec_sed_doc(
        doc=sed_doc,
        working_dir=ecoli_archive_dirpath,
        base_out_path=outputs_dirpath,
        config=sim_config,
    )


with open('sim_pipe/files/models/ecoli_modelout.txt', 'r') as f:
    lines = f.readlines()


r = list(range(20))
ranged = [str(v) for v in r]
data_list = [line.strip() for line in lines]

mindatp_data = []

minESoluationData = []


for d in data_list:
    if d.startswith('MinD_ATP(front)'):
        mindatp_data.append(d)


def get_variable_data(_data_list: list, var_name: str):
    data = []
    for d in _data_list:
        if d.startswith(var_name):
            data.append(d)
    return data


coordinates = []
three_d_data = {'MinD_ATP(front)': []}
for line in mindatp_data:
    data = line[len(list(three_d_data.keys())[0]):]
    data = data[1:]
    three_d_data[list(three_d_data.keys())[0]] = data
    coordinates.append(tuple(data.split(' ')))

three_d_data[list(three_d_data.keys())[0]] = coordinates

# print(three_d_data)

input_file_data = InputFileData('sim_pipe/files/models/ecoli_modelout.txt')
box_size = 1.
smoldyn_data = SmoldynData(
    smoldyn_file=input_file_data,
    spatial_units=UnitData("m"),
    time_units=UnitData("s")
)

c = SmoldynConverter(smoldyn_data)
translation_magnitude = -box_size / 2
filtered_data = c.filter_data([
    TranslateFilter(
        translation_per_type={},
        default_translation=translation_magnitude * np.ones(3)
    ),
])
BinaryWriter.save(filtered_data, "sim_pipe/andrews_ecoli_spatial_smoldyn", validate_ids=False)



# sim_language = [ModelLanguage.Smoldyn]

# ecoli_model_from_utils = Model(source=model_fp, language=sim_language)

# sim_task = Task(model=ecoli_model_from_utils)


# df = bioSim.combine.get_smoldyn_output(cmd, False, (4000, ))


# simulation_from_file = create_simulation_from_file()

# simulation_configuration = bioSim.combine.read_smoldyn_simulation_configuration(model_fp)

# results, logs = run_simulation_from_sed_doc()
# simulation_from_file.runSim()
