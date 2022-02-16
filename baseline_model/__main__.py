from baseline_model import default_run_args
from baseline_model.experiment import standard_run
from cadCAD_tools.execution import easy_run
from datetime import datetime
import click
import os


@click.command()
@click.option('-e', '--experiment-run', 'experiment_run',
              default=False,
              is_flag=True,
              help="Make an experiment run instead")
def main(experiment_run: bool) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if experiment_run is False:
        df = easy_run(*default_run_args)
        df.to_pickle(
            f"data/simulations/single-run-{timestamp}.pkl.gz", compression="gzip")
    else:
        df = standard_run()
        df.to_pickle(
            f"data/simulations/multi-run-{timestamp}.pkl.gz", compression="gzip")


if __name__ == "__main__":
    main()
