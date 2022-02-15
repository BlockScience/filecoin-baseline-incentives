from baseline_model import default_run_args
from cadCAD_tools.execution import easy_run
from datetime import datetime
import click
import os


@click.command()
def main() -> None:
    df = easy_run(*default_run_args)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    df.to_pickle(f"data/simulations/{timestamp}.pkl.gz", compression="gzip")


if __name__ == "__main__":
    main()