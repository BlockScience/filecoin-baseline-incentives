import pandas as pd
from consensus_pledge_model.params import INITIAL_STATE
from consensus_pledge_model.params import SINGLE_RUN_PARAMS
from consensus_pledge_model.structure import CONSENSUS_PLEDGE_DEMO_BLOCKS
from cadCAD_tools import easy_run


def standard_run() -> pd.DataFrame:
       N_timesteps = 360
       N_samples = 1
       # %%
       sweep_params = {k: [v] for k, v in SINGLE_RUN_PARAMS.items()}

       sim_args = (INITIAL_STATE,
              sweep_params, 
              CONSENSUS_PLEDGE_DEMO_BLOCKS, 
              N_timesteps,
              N_samples)
       sim_df = easy_run(*sim_args)
       return sim_df
