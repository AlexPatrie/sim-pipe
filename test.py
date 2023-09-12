import os
from datetime import datetime
import numpy as np
from biosimulators_utils.config import Config
from biosimulators_utils.report.io import ReportFormat
from simulariumio.data_objects import TrajectoryData, AgentData, MetaData, CameraData, ModelMetaData
from sim_pipe.data_generators.smoldyn_data_generator import SmoldynDataGenerator


def get_run_id(fp: str) -> str:
    i = 0
    files = os.listdir(fp)
    if str(i) in files:
         i = int(files[-1]) + 1
    return str(i)


def main():
    if os.path.exists('biosimulators_Andrews_ecoli.simularium'):
        os.remove('biosimulators_Andrews_ecoli.simularium')

    archive = 'sim_pipe/files/archives/Andrews_ecoli_0523.omex'
    project_root = os.getcwd()
    root_output_dir = os.path.join(project_root, 'test_simulation_outputs')
    run_id = get_run_id(root_output_dir)
    output_dir = os.path.join(root_output_dir, run_id)

    conf = Config(REPORT_FORMATS=[ReportFormat.csv])

    generator = SmoldynDataGenerator(
        archive_fp=archive,
        output_dir=output_dir,
        config=conf
    )

    trajectory_title = "Andrews_ecoli_trajectory"
    sim_trajectory = generator.generate_trajectory_object(title=trajectory_title)

    simularium_dir = os.path.join(project_root, "simularium_files")
    simularium_fname = "biosimulators_Andrews_ecoli"
    simularium_fp = generator.prepare_simularium_fp(simularium_dir, simularium_fname)

    generator.convert(sim_trajectory, simularium_fp)


if __name__ == "__main__":
    main()

# run_id = str(datetime.today().minute) + '_' + str(datetime.today().second)
