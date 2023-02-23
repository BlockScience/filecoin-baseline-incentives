# %%
import sys
sys.path.append('../')

# %%
from consensus_pledge_model.params import CONSENSUS_PLEDGE_DEMO_INITIAL_STATE
from consensus_pledge_model.params import CONSENSUS_PLEDGE_DEMO_SINGLE_RUN_PARAMS
from consensus_pledge_model.structure import CONSENSUS_PLEDGE_DEMO_BLOCKS
from cadCAD_tools import easy_run

N_timesteps = 10
N_samples = 1
# %%

sweep_params = {k: [v] for k, v in CONSENSUS_PLEDGE_DEMO_SINGLE_RUN_PARAMS.items()}

sim_args = (CONSENSUS_PLEDGE_DEMO_INITIAL_STATE,
            sweep_params, 
            CONSENSUS_PLEDGE_DEMO_BLOCKS, 
            N_timesteps,
            N_samples)
sim_df = easy_run(*sim_args)

# %%
