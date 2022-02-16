# filecoin-baseline-incentives
Interactive Calculator for the economic incentives around the Filecoin Baseline Minting

## How to run it

- Option 1 (CLI): Just pass `python -m baseline_model`
This will generate an pickled file at `data/simulations/` using the default single run
system parameters & initial state.
    - To perform a multiple run, pass `python -m baseline_model -e`
- Option 2 (cadCAD-tools easy run method): Import the objects at `baseline_model/__init__.py`
and use them as arguments to the `cadCAD_tools.execution.easy_run` method. Refer to `baseline_model/__main__.py` to an example.
## File structure

- baseline_model/: the `cadCAD` model as encapsulated by a Python Module
- data/: Simulation / Post-processed datasets
- notebooks/: 