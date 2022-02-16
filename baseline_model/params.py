from cmath import nan
from math import ceil
from baseline_model.types import BaselineMinting, BaselineModelState, BaselineModelParams, BaselineModelSweepParams, GrowthScenario, Reward, SimpleMinting
from cadCAD_tools.preparation import sweep_cartesian_product
DAYS_PER_TIMESTEP = 30
YEAR = 365.25
DAYS_AFTER_LAUNCH = 600
SIMULATION_TIME_IN_YEARS = 6

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
                                   network_power=12000,  # TODO
                                   baseline=9500,  # TODO
                                   cumm_capped_power=12000 / 2,  # TODO
                                   effective_network_time=1.4,  # TODO
                                   reward=Reward()
                                   )

TIMESTEPS = int(ceil(SIMULATION_TIME_IN_YEARS * YEAR) / DAYS_PER_TIMESTEP)
SAMPLES = 1
