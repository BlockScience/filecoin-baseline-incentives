# %%

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pandas as pd

from cadCAD_tools.execution import easy_run
from consensus_pledge_model.types import ConsensusPledgeSweepParams, BehaviouralParams
from consensus_pledge_model.params import INITIAL_STATE, SINGLE_RUN_PARAMS, TIMESTEPS, SAMPLES
from consensus_pledge_model.structure import CONSENSUS_PLEDGE_DEMO_BLOCKS
from utils import load_constants


C = CONSTANTS = load_constants()



def run_cadcad_model(new_sector_rb_onboarding_rate,
                     new_sector_quality_factor,
                     new_sector_lifetime):
    
    RESULTS = []

    ## Scenario 1 - User

    user_behaviour_params = BehaviouralParams('user',
                                              new_sector_rb_onboarding_rate,
                                              new_sector_quality_factor,
                                              new_sector_lifetime,
                                              0.02,
                                              new_sector_lifetime)

    params = SINGLE_RUN_PARAMS.copy()
    params["behavioural_params"] = {TIMESTEPS: user_behaviour_params}

    
    SWEEP_RUN_PARAMS = ConsensusPledgeSweepParams(**{k: [v] for k, v in params.items()})
    RUN_ARGS = (INITIAL_STATE, SWEEP_RUN_PARAMS, CONSENSUS_PLEDGE_DEMO_BLOCKS, TIMESTEPS, SAMPLES)
    RESULTS.append(easy_run(*RUN_ARGS))

    # Post-process results
    df = post_process_results(pd.concat(RESULTS))
    df = df.assign(scenario='user')
    
    # Return relevant scenarios
    return df.query('timestep > 0')

def post_process_results(results):
    dfs = [
        results,
        results.reward.map(lambda x: x.__dict__).apply(pd.Series)
    ]

    DROP_COLS = ["reward", "simple_mechanism", "baseline_mechanism"]

    df = (
        pd.concat(dfs, axis=1)
        .assign(simple_reward=lambda df: df.reward.map(lambda x: x.simple_reward))
        .assign(baseline_reward=lambda df: df.reward.map(lambda x: x.baseline_reward))
        .assign(fil_locked=lambda df: df.token_distribution.map(lambda x: x.locked))
        .assign(fil_collateral=lambda df: df.token_distribution.map(lambda x: x.collateral))
        .assign(fil_locked_reward=lambda df: df.token_distribution.map(lambda x: x.locked_rewards))
        .assign(block_reward=lambda x: x.simple_reward + x.baseline_reward)
        .assign(marginal_reward=lambda x: x.block_reward / x.power_qa)
        .assign(years_passed=lambda x: x.days_passed / C["days_per_year"])
        .drop(columns=DROP_COLS)
    )
    return df


def map_args_to_scenario(row):
    label, baseline_activated = row["label"], row["baseline_activated"]
    if label == "pessimistic" and baseline_activated:
        return "user"
    elif label == "pessimistic" and not baseline_activated:
        return "user-baseline-deactivated"
    elif label == "optimistic" and baseline_activated:
        return "optimistic"
    elif label == "baseline" and baseline_activated:
        return "baseline"
    else:
        return label, baseline_activated

# %%
sim_df = run_cadcad_model(10, 2, 180)
# %%
