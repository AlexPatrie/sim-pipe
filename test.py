import os
from datetime import datetime
import numpy as np
from biosimulators_utils.config import Config
from biosimulators_utils.report.io import ReportFormat
from simulariumio.data_objects import TrajectoryData, AgentData, MetaData, CameraData, ModelMetaData

from sim_pipe.data_generators.smoldyn_data_generator import SmoldynDataGenerator


def GET_RUN_ID(fp: str) -> str:
    i = 0
    files = os.listdir(fp)
    if str(i) in files:
         i = int(files[-1]) + 1
    return str(i)


def main():
    if os.path.exists('biosimulators_Andrews_ecoli.simularium'):
        os.remove('biosimulators_Andrews_ecoli.simularium')
    run_id = str(datetime.today().minute) + '_' + str(datetime.today().second)
    archive = 'sim_pipe/files/archives/Andrews_ecoli_0523.omex'
    project_root = os.getcwd()
    root_output_dir = os.path.join(project_root, 'test_simulation_outputs')
    output_dir = os.path.join(root_output_dir, run_id)

    conf = Config(REPORT_FORMATS=[ReportFormat.csv])

    generator = SmoldynDataGenerator(
        archive_fp=archive,
        output_dir=output_dir,
        config=conf
    )

    trajectory_title = "Andrews_ecoli"

    sim_trajectory = generator.generate_trajectory_object(title=trajectory_title)

    simularium_fname = os.path.join(project_root, "biosimulators_Andrews_ecoli")
    generator.convert(sim_trajectory, simularium_fname)


if __name__ == "__main__":
    main()

