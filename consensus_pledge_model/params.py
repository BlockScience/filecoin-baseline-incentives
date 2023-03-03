from cmath import nan
from math import ceil
from consensus_pledge_model.types import BaselineMinting, BaselineModelState, BaselineModelParams, BaselineModelSweepParams, GrowthScenario, Reward, SimpleMinting
from cadCAD_tools.preparation import sweep_cartesian_product

from consensus_pledge_model.types import ConsensusPledgeDemoState, ConsensusPledgeParams, ConsensusPledgeSweepParams
from consensus_pledge_model.types import QA_PiB, PiB_per_Day, PiB, Days, FIL, FIL_per_QA_PiB
from consensus_pledge_model.types import AggregateSector, TokenDistribution
from consensus_pledge_model.types import AggregateSectorList

# TODO: Upgrade to the Consensus Pledge Model
# TODO: pinpoint the sources for the numerical constants

# TODO: refactor
# DAYS_PER_TIMESTEP = 1
YEAR = 365.25
# SIMULATION_TIME_IN_YEARS = 6
TIMESTEP_IN_DAYS = 1
# TIMESTEPS = int(ceil(SIMULATION_TIME_IN_YEARS * YEAR) / DAYS_PER_TIMESTEP)
TIMESTEPS = 10

BLOCKS_SINCE_LAUNCH = 1_563_129 # Block height used as an reference point
DAYS_AFTER_LAUNCH = (BLOCKS_SINCE_LAUNCH * 30) / (60 * 60 * 24) # Days after launch
YEARS_AFTER_LAUNCH = DAYS_AFTER_LAUNCH / YEAR

INITIAL_NETWORK_POWER: QA_PiB = 15574 # QA PiB

# Guess-estimate
INITIAL_BASELINE: PiB = 8000 # RBP PiB 

# Guess-estimate
INITIAL_CUMM_CAPPED_POWER = INITIAL_NETWORK_POWER * YEARS_AFTER_LAUNCH / 2 

# Guess-estimate
INITIAL_EFFECTIVE_NETWORK_TIME: Days = 1.92 * 365.25


SAMPLES = 1

"""
Note: the previous code from the Baseline Edu Calculator ends here.
"""

# TODO: move from `hack` definitions towards `guess` or `estimate` ones.
# INITIAL_AGGREGATE_SECTORS = AggregateSectorList([]) # Source: hack
INITIAL_AGGREGATE_SECTORS = []

INITIAL_TOKEN_DISTRIBUTION: TokenDistribution = TokenDistribution(
    minted=0.0,
    vested=0.0,
    collateral=0.0,
    locked_rewards=0.0,
    burnt=0.0
)

INITIAL_REWARDS: FIL = 0.0 # Source: hack
INITIAL_MINTED = BaselineMinting().issuance(INITIAL_EFFECTIVE_NETWORK_TIME)
INITIAL_MINTED += SimpleMinting().issuance(INITIAL_EFFECTIVE_NETWORK_TIME)
INITIAL_VESTED: FIL = 0.0 # Source: hack
INITIAL_BURNT: FIL = 0.0 # Source: hack
INITIAL_TOKEN_DISTRIBUTION.update_distribution(new_vested=INITIAL_VESTED,
                                               minted=INITIAL_MINTED,
                                               aggregate_sectors=INITIAL_AGGREGATE_SECTORS,
                                               marginal_burn=INITIAL_BURNT)

DEMO_VESTING_SCHEDULE: dict[Days, FIL] = {} # TODO: fill in
AVERAGE_QUALITY_FACTOR = 3.0

INITIAL_ONBOARDING_CONSENSUS_PLEDGE: FIL_per_QA_PiB = 0.0 # Source: hack
INITIAL_ONBOARDING_STORAGE_PLEDGE: FIL_per_QA_PiB = 0.0 # Source: hack

INITIAL_STATE = ConsensusPledgeDemoState(
    days_passed=0,
    delta_days=TIMESTEP_IN_DAYS,
    aggregate_sectors=INITIAL_AGGREGATE_SECTORS,
    token_distribution=INITIAL_TOKEN_DISTRIBUTION,
    power_qa=INITIAL_NETWORK_POWER,
    power_rb=INITIAL_NETWORK_POWER / AVERAGE_QUALITY_FACTOR,
    baseline=INITIAL_BASELINE,
    cumm_capped_power=INITIAL_CUMM_CAPPED_POWER,
    effective_days_passed=INITIAL_EFFECTIVE_NETWORK_TIME,
    reward=Reward(0.0, 0.0), # HACK
    storage_pledge_per_new_qa_power=INITIAL_ONBOARDING_CONSENSUS_PLEDGE,
    consensus_pledge_per_new_qa_power=INITIAL_ONBOARDING_STORAGE_PLEDGE
)

LINEAR_DURATION: Days = 180 # Source: Spec

SINGLE_RUN_PARAMS = ConsensusPledgeParams(
    timestep_in_days=TIMESTEP_IN_DAYS,
    vesting_schedule=DEMO_VESTING_SCHEDULE, # Source: Guess
    target_locked_supply=0.3, # Source: Spec
    storage_pledge_factor=20, # Source: Spec 
    simple_mechanism=SimpleMinting(), # TODO: re-evaluate it
    baseline_mechanism=BaselineMinting(), # TODO: re-evaluate it
    baseline_activated=True,
    linear_duration=LINEAR_DURATION, 
    immediate_release_fraction=0.25, # Source: Spec
    new_sector_lifetime=LINEAR_DURATION,
    onboarding_rate=INITIAL_NETWORK_POWER * 0.1, # Source: Guess
    onboarding_quality_factor=2.0, # Source: Guess
    renewal_probability=0.01 # Source: Guess
)


MULTI_RUN_PARAMS = ConsensusPledgeSweepParams(**{k: [v] for k, v in SINGLE_RUN_PARAMS.items()})