from sim_pipe.data_generators.smoldyn_data_generator import SmoldynDataGenerator, SimulationSetup
import os


OUTPUTS = SimulationSetup.outputs_dirpath.value
MODEL_FP = SimulationSetup.model_fp.value
MODEL_OUTPUT_FP = 'sim_pipe/files/models/ecoli_modelout.txt'
SIMULARIUM_FILENAME = os.path.join(OUTPUTS, 'ecoli_spatial_0')
BOX_SIZE = 1.
N_DIM = 3

generator = SmoldynDataGenerator(OUTPUTS)

generator.run_simulation_from_smoldyn_file(MODEL_FP)

generator.generate_simularium_file(MODEL_OUTPUT_FP, SIMULARIUM_FILENAME, BOX_SIZE, N_DIM)

