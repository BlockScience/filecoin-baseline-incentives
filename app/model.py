
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import pandas as pd
from cadCAD_tools.execution import easy_run
from consensus_pledge_model.types import ConsensusPledgeSweepParams, BehaviouralParams
from consensus_pledge_model.params import INITIAL_STATE, MULTI_RUN_PARAMS, TIMESTEPS, SAMPLES
from consensus_pledge_model.structure import CONSENSUS_PLEDGE_DEMO_BLOCKS
from utils import load_constants
from copy import deepcopy
from cadCAD_tools.preparation import sweep_cartesian_product

C = CONSTANTS = load_constants()



def run_cadcad_model(duration_1,
                     new_sector_rb_onboarding_rate_1,
                     new_sector_quality_factor_1,
                     new_sector_lifetime_1,
                     renewal_probability_1,
                     new_sector_rb_onboarding_rate_2,
                     new_sector_quality_factor_2,
                     new_sector_lifetime_2,
                     renewal_probability_2):
    
    ## Scenario 1 - User

    first_year = BehaviouralParams('first_year',
                                              new_sector_rb_onboarding_rate_1,
                                              new_sector_quality_factor_1,
                                              new_sector_lifetime_1,
                                              renewal_probability_1,
                                              new_sector_lifetime_1)
    second_year = BehaviouralParams('second_year',
                                              new_sector_rb_onboarding_rate_2,
                                              new_sector_quality_factor_2,
                                              new_sector_lifetime_2,
                                              renewal_probability_2,
                                              new_sector_lifetime_2)
    params = deepcopy(MULTI_RUN_PARAMS)
    params["behavioural_params"] = [{duration_1: first_year,
                                    10000: second_year}]

    RUN_ARGS = (deepcopy(INITIAL_STATE), sweep_cartesian_product(params), CONSENSUS_PLEDGE_DEMO_BLOCKS, TIMESTEPS, SAMPLES)
    
    df = easy_run(*RUN_ARGS)

    # Post-process results
    df = post_process_results(df)
    df['scenario'] = ''
    df.loc[df.target_locked_supply == 0.3, 'scenario'] = 'user'
    df.loc[df.target_locked_supply == 0.0, 'scenario'] = 'user-deactivated'
    
    # Return relevant scenarios
    return df.query('timestep > 1')

def post_process_results(df):

    DROP_COLS = ["reward", 
                 "simple_mechanism", 
                 "baseline_mechanism", 
                 "token_distribution",
                 "aggregate_sectors",
                 "behavioural_params",
                 "vesting_schedule",
                 "behaviour"]

    df = (df
        .assign(simple_reward=lambda df: df.reward.map(lambda x: x.simple_reward))
        .assign(baseline_reward=lambda df: df.reward.map(lambda x: x.baseline_reward))
        .assign(fil_locked=lambda df: df.token_distribution.map(lambda x: x.locked))
        .assign(fil_collateral=lambda df: df.token_distribution.map(lambda x: x.collateral))
        .assign(fil_locked_reward=lambda df: df.token_distribution.map(lambda x: x.locked_rewards))
        .assign(fil_circulating=lambda df: df.token_distribution.map(lambda x: x.circulating))
        .assign(fil_available=lambda df: df.token_distribution.map(lambda x: x.available))
        .assign(fil_vested=lambda df: df.token_distribution.map(lambda x: x.vested))
        .assign(fil_minted=lambda df: df.token_distribution.map(lambda x: x.minted))
        .assign(block_reward=lambda x: x.simple_reward + x.baseline_reward)
        .assign(marginal_reward=lambda x: x.block_reward / x.power_qa)
        .assign(years_passed=lambda x: x.days_passed / C["days_per_year"])
        .assign(critical_cost=lambda df: (df.power_qa * 0.33) * (df.consensus_pledge_per_new_qa_power + df.storage_pledge_per_new_qa_power))
        .assign(circulating_surplus=lambda df: df.fil_circulating / df.critical_cost - 1)
        .assign(circulating_supply=lambda df: df.fil_circulating / df.fil_available)
        .assign(locked_supply=lambda df: df.fil_locked / df.fil_available)
        .drop(columns=DROP_COLS)
    )
    return df
