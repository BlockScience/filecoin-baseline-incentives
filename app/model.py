import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pandas as pd
import streamlit as st

from cadCAD_tools.execution import easy_run
from cadCAD_tools.preparation import sweep_cartesian_product
from baseline_model.params import INITIAL_STATE, TIMESTEPS, SAMPLES, DAYS_PER_TIMESTEP
from baseline_model.structure import BLOCKS
from baseline_model.types import BaselineMinting, BaselineModelSweepParams, GrowthScenario, SimpleMinting
from utils import load_constants


C = CONSTANTS = load_constants()


@st.cache
def run_cadcad_model(
    fall_after_beginning,
    growth_fall,
    stable_after_fall,
    growth_stable,
    take_off_after_stable,
    growth_take_off,
    steady_after_take_off,
    growth_steady,
):
    NPO = C["network_power"]["optimistic"]
    RESULTS = []
    # Run pessimistic, optimistic scenarios
    SCENARIOS = [
        GrowthScenario(
            label="pessimistic",
            fall_after_beginning=fall_after_beginning,
            stable_after_fall=stable_after_fall,
            take_off_after_stable=take_off_after_stable,
            steady_after_take_off=steady_after_take_off,
            growth_fall=growth_fall,
            growth_stable=growth_stable,
            growth_take_off=growth_take_off,
            growth_steady=growth_steady,
        ),
        GrowthScenario(
            label="optimistic",
            fall_after_beginning=NPO["fall_after_beginning"],
            stable_after_fall=NPO["stable_after_fall"],
            take_off_after_stable=NPO["take_off_after_stable"],
            steady_after_take_off=NPO["steady_after_take_off"],
            growth_fall=NPO["growth_fall"],
            growth_stable=NPO["growth_stable"],
            growth_take_off=NPO["growth_take_off"],
            growth_steady=NPO["growth_steady"],
        ),
    ]
    RAW_PARAMS = BaselineModelSweepParams(
        timestep_in_days=[DAYS_PER_TIMESTEP],
        baseline_activated=[True, False],
        network_power_scenario=SCENARIOS,
        simple_mechanism=[SimpleMinting()],
        baseline_mechanism=[BaselineMinting()],
    )
    PARAMS = sweep_cartesian_product(RAW_PARAMS)
    RUN_ARGS = (INITIAL_STATE, PARAMS, BLOCKS, TIMESTEPS, SAMPLES)
    RESULTS.append(easy_run(*RUN_ARGS))
    # Run baseline scenario
    RUN_ARGS = (
        {**INITIAL_STATE, "network_power": INITIAL_STATE["baseline"]},
        {**RAW_PARAMS, "baseline_activated": [True], "network_power_scenario": [GrowthScenario("baseline")]},
        BLOCKS,
        TIMESTEPS,
        SAMPLES,
    )
    RESULTS.append(easy_run(*RUN_ARGS))
    # Post-process results
    df = post_process_results(pd.concat(RESULTS))
    df = df.assign(scenario=df.apply(map_args_to_scenario, axis=1))
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
    ]


def post_process_results(results):
    dfs = [
        results,
        results.reward.map(lambda x: x.__dict__).apply(pd.Series),
        results.network_power_scenario.map(lambda x: x.__dict__).apply(pd.Series),
    ]

    DROP_COLS = ["reward", "network_power_scenario", "simple_mechanism", "baseline_mechanism"]

    df = (
        pd.concat(dfs, axis=1)
        .drop(columns=DROP_COLS)
        .assign(block_reward=lambda x: x.simple_reward + x.baseline_reward)
        .assign(marginal_reward=lambda x: x.block_reward / x.network_power)
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
