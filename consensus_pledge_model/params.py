from cmath import nan
from math import ceil
from consensus_pledge_model.types import BaselineMinting, BaselineModelState, BaselineModelParams, BaselineModelSweepParams, GrowthScenario, Reward, SimpleMinting
from cadCAD_tools.preparation import sweep_cartesian_product

DAYS_PER_TIMESTEP = 30
YEAR = 365.25
SIMULATION_TIME_IN_YEARS = 6

BLOCKS_SINCE_LAUNCH = 1_563_129 # Block height used as an reference point
DAYS_AFTER_LAUNCH = (BLOCKS_SINCE_LAUNCH * 30) / (60 * 60 * 24) # Days after launch
YEARS_AFTER_LAUNCH = DAYS_AFTER_LAUNCH / YEAR

INITIAL_NETWORK_POWER = 15574 # QA PiB

# Guess-estimate
INITIAL_BASELINE = 8000 # QA PiB 

# Guess-estimate
INITIAL_CUMM_CAPPED_POWER = INITIAL_NETWORK_POWER * YEARS_AFTER_LAUNCH / 2 

# Guess-estimate
INITIAL_EFFECTIVE_NETWORK_TIME = 1.92

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
