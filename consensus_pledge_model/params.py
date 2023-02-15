from cmath import nan
from math import ceil
from consensus_pledge_model.types import BaselineMinting, BaselineModelState, BaselineModelParams, BaselineModelSweepParams, GrowthScenario, Reward, SimpleMinting
from cadCAD_tools.preparation import sweep_cartesian_product

from consensus_pledge_model.types import ConsensusPledgeDemoState, ConsensusPledgeParams
from consensus_pledge_model.types import QA_PiB, PiB_per_Day, PiB, Days, FIL
from consensus_pledge_model.types import AggregateSector, TokenDistribution

# TODO: Upgrade to the Consensus Pledge Model
# TODO: pinpoint the sources for the numerical constants

DAYS_PER_TIMESTEP = 30
YEAR = 365.25
SIMULATION_TIME_IN_YEARS = 6

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

SCENARIOS = [
    GrowthScenario(label='optimistic',
                   fall_after_beginning=1.0 * YEAR + DAYS_AFTER_LAUNCH,
                   stable_after_fall=1.0 * YEAR,
                   take_off_after_stable=1.0 * YEAR,
                   steady_after_take_off=1.0 * YEAR,
                   growth_fall=1.05,
                   growth_stable=1.05,
                   growth_take_off=1.05,
                   growth_steady=1.05
                   ),
    GrowthScenario(label='pessimistic',
                   fall_after_beginning=0.5 * YEAR + DAYS_AFTER_LAUNCH,
                   stable_after_fall=0.5 * YEAR,
                   take_off_after_stable=3.0 * YEAR,
                   steady_after_take_off=0.5 * YEAR,
                   growth_fall=0.0,
                   growth_stable=1.0,
                   growth_take_off=4.0,
                   growth_steady=1.0
                   )
]


RAW_PARAMS = BaselineModelSweepParams(timestep_in_days=[DAYS_PER_TIMESTEP],
                                      baseline_activated=[True, False],
                                      network_power_scenario=SCENARIOS,
                                      simple_mechanism=[SimpleMinting()],
                                      baseline_mechanism=[BaselineMinting()])

PARAMS = sweep_cartesian_product(RAW_PARAMS)

INITIAL_STATE = BaselineModelState(days_passed=DAYS_AFTER_LAUNCH,
                                   delta_days=nan,
                                   network_power=INITIAL_NETWORK_POWER,
                                   baseline=INITIAL_BASELINE,
                                   cumm_capped_power=INITIAL_CUMM_CAPPED_POWER, 
                                   effective_network_time=INITIAL_EFFECTIVE_NETWORK_TIME,
                                   reward=Reward()
                                   )

TIMESTEPS = int(ceil(SIMULATION_TIME_IN_YEARS * YEAR) / DAYS_PER_TIMESTEP)
SAMPLES = 1

# TODO: move from `hack` definitions towards `guess` or `estimate` ones.
INITIAL_AGGREGATE_SECTORS: list[AggregateSector] = [] # Source: hack
INITIAL_TOKEN_DISTRIBUTION: TokenDistribution = TokenDistribution(
    minted=None,
    vested=None,
    collateral=None,
    locked_rewards=None,
    burnt=None
)

INITIAL_REWARDS = 0.0 # Source: hack
INITIAL_VESTED = 0.0 # Source: hack
INITIAL_BURNT = 0.0 # Source: hack
INITIAL_TOKEN_DISTRIBUTION.update_distribution(new_rewards=INITIAL_REWARDS,
                                               new_vested=INITIAL_VESTED,
                                               aggregate_sectors=INITIAL_AGGREGATE_SECTORS,
                                               marginal_burn=INITIAL_BURNT)

DEMO_VESTING_SCHEDULE: dict[Days, FIL] = None
AVERAGE_QUALITY_FACTOR = 3.0

CONSENSUS_PLEDGE_DEMO_INITIAL_STATE = ConsensusPledgeDemoState(
    days_passed=0,
    delta_days=0,
    aggregate_sectors=INITIAL_AGGREGATE_SECTORS,
    token_distribution=INITIAL_TOKEN_DISTRIBUTION,
    power_qa=INITIAL_NETWORK_POWER,
    power_rb=INITIAL_NETWORK_POWER / AVERAGE_QUALITY_FACTOR,
    baseline=INITIAL_BASELINE,
    cumm_capped_power=INITIAL_CUMM_CAPPED_POWER,
    effective_days_passed=INITIAL_EFFECTIVE_NETWORK_TIME,
    reward=Reward()
)

CONSENSUS_PLEDGE_DEMO_SINGLE_RUN_PARAMS = ConsensusPledgeParams(
    VestingSchedule=DEMO_VESTING_SCHEDULE, # Source: Guess
    target_locked_supply=0.3, # Source: Spec
    storage_pledge_factor=20, # Source: Spec
    linear_duration=180, # Source: Spec
    immediate_release_fraction=0.25, # Source: Spec
    onboarding_rate=INITIAL_NETWORK_POWER * 0.1, # Source: Guess
    onboarding_quality_factor=2.0, # Source: Guess
    renewal_probability=0.01 # Source: Guess
)