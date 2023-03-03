import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pandas as pd
import streamlit as st

from cadCAD_tools.execution import easy_run
from cadCAD_tools.preparation import sweep_cartesian_product
from consensus_pledge_model.params import *
from consensus_pledge_model.structure import CONSENSUS_PLEDGE_DEMO_BLOCKS
from consensus_pledge_model.types import BaselineMinting, BaselineModelSweepParams, GrowthScenario, SimpleMinting
from utils import load_constants


C = CONSTANTS = load_constants()



def run_cadcad_model():
    RESULTS = []
    SWEEP_RUN_PARAMS = sweep_cartesian_product(MULTI_RUN_PARAMS)
    RUN_ARGS = (INITIAL_STATE, SWEEP_RUN_PARAMS, CONSENSUS_PLEDGE_DEMO_BLOCKS, TIMESTEPS, SAMPLES)
    RESULTS.append(easy_run(*RUN_ARGS))
    # Run baseline scenario
    RUN_ARGS = (
        {**INITIAL_STATE, "network_power": INITIAL_STATE["baseline"]},
        {**SWEEP_RUN_PARAMS, "baseline_activated": [True], "network_power_scenario": [GrowthScenario("baseline")]},
        CONSENSUS_PLEDGE_DEMO_BLOCKS,
        TIMESTEPS,
        SAMPLES,
    )
    RESULTS.append(easy_run(*RUN_ARGS))
    # Post-process results
    df = post_process_results(pd.concat(RESULTS))
    df = df.assign(scenario='baseline')
    # df = df.assign(scenario=df.apply(map_args_to_scenario, axis=1)) TODO: review
    # Compute mining utility
    baseline_marginal_reward = df[df["scenario"] == "baseline"]["marginal_reward"]
    num_scens = len(df["scenario"].unique())
    mining_utility_denom = np.array(num_scens * baseline_marginal_reward.tolist())
    df = df.assign(mining_utility=df["marginal_reward"] / mining_utility_denom)
    # Return relevant scenarios
    return df[
        df["scenario"].isin(
            [
                "user",
                "user-baseline-deactivated",
                "optimistic",
                "baseline",
            ]
        )
    ].query("timestep > 0")


def post_process_results(results):
    dfs = [
        results,
        results.reward.map(lambda x: x.__dict__).apply(pd.Series)
    ]

    DROP_COLS = ["reward", "simple_mechanism", "baseline_mechanism"]

    df = (
        pd.concat(dfs, axis=1)
        .drop(columns=DROP_COLS)
        .assign(block_reward=lambda x: x.simple_reward + x.baseline_reward)
        .assign(marginal_reward=lambda x: x.block_reward / x.power_qa)
        .assign(years_passed=lambda x: x.days_passed / C["days_per_year"])
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
