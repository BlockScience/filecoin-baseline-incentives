# filecoin-baseline-incentives
Interactive Calculator for the economic incentives around the Filecoin Baseline Minting based on cadCAD + Streamlit.

## How to run it

- Option 1 (CLI): Just pass `python -m consensus_pledge_model`
This will generate an pickled file at `data/simulations/` using the default single run
system parameters & initial state.
    - To perform a multiple run, pass `python -m consensus_pledge_model -e`
- Option 2 (cadCAD-tools easy run method): Import the objects at `consensus_pledge_model/__init__.py`
and use them as arguments to the `cadCAD_tools.execution.easy_run` method. Refer to `consensus_pledge_model/__main__.py` to an example.
- Option 3 (Streamlit, local)
- Option 4 (Streamlit, cloud)
    1. Fork the repo
    2. Go to https://share.streamlit.io/ and log in
    3. Create an app for the repo pointing to `app/main.py`
    4. **Make sure to use Python 3.9 on the Advanced Settings!**
    5. Wait a bit and done!
## File structure

- `app/`: The `streamlit` app
- `consensus_pledge_model/`: the `cadCAD` model as encapsulated by a Python Module
- `data/`: Simulation / Post-processed datasets
- `notebooks/`: 
- `scripts/`: 
- `tests/`: 