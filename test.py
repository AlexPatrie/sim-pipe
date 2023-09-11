import os
from datetime import datetime
import numpy as np
from biosimulators_utils.config import Config
from biosimulators_utils.report.io import ReportFormat
from simulariumio.data_objects import TrajectoryData, AgentData, MetaData, CameraData, ModelMetaData

from sim_pipe.data_generators.smoldyn_data_generator import SmoldynDataGenerator


def __run_id(fp: str) -> int:
    i = 0
    if os.path.exists(os.path.join(fp, str(i))):
        i += 1
    return i


def main():
    run_id = str(datetime.today().minute) + '_' + str(datetime.today().second)
    archive = 'sim_pipe/files/archives/Andrews_ecoli_0523.omex'
    root_output_dir = os.path.join(os.getcwd(), 'test_simulation_outputs')
    output_dir = os.path.join(root_output_dir, run_id)

    conf = Config(REPORT_FORMATS=[ReportFormat.csv])

    generator = SmoldynDataGenerator(
        archive_fp=archive,
        output_dir=output_dir,
        config=conf
    )

    df = generator.get_result_dataframe()

    timestamps = df.pop('Time').values
    agents = df.values

    box_size = 100
    total_steps = 100
    n_agents = len(agents)
    type_names = df.columns
    min_radius = 5
    max_radius = 10

    default_data = TrajectoryData(
        meta_data=MetaData(
            box_size=np.array([box_size, box_size, box_size]),
            camera_defaults=CameraData(
                position=np.array([10.0, 0.0, 200.0]),
                look_at_position=np.array([10.0, 0.0, 0.0]),
                fov_degrees=60.0,
            ),
            trajectory_title="Some parameter set",
            model_meta_data=ModelMetaData(
                title="Spatiotemporal oscillations in the E. coli Min system",
                version="1.0",
                authors="Steve Andrews et al.",
                description=(
                    "A Smoldyn example model of the E. coli Min system, which is used to find the cell center during cell division."
                ),
                doi="10.1016/j.bpj.2016.02.002",
                source_code_url="https://github.com/simularium/simulariumio",
                source_code_license_url="https://github.com/simularium/simulariumio/blob/main/LICENSE",
                input_data_url="https://allencell.org/path/to/native/engine/input/files",
                raw_output_data_url="https://allencell.org/path/to/native/engine/output/files",
            ),
        ),
        agent_data=AgentData(
            times=timestamps,
            n_agents=np.array(total_steps * [n_agents]),
            viz_types=np.array(total_steps * [n_agents * [1000.0]]),  # default viz type = 1000
            unique_ids=np.array(total_steps * [list(range(n_agents))]),
            types=type_names,
            positions=np.random.uniform(size=(total_steps, n_agents, 3)) * box_size - box_size * 0.5,
            radii=(max_radius - min_radius) * np.random.uniform(size=(total_steps, n_agents)) + min_radius
        )
    )

    print(default_data)


if __name__ == "__main__":
    main()

