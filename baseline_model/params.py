from math import ceil
from baseline_model.types import BaselineMinting, BaselineModelState, BaselineModelParams, GrowthScenario, Reward, SimpleMinting

DAYS_PER_TIMESTEP = 30
YEAR = 365.25
SIMULATION_TIME_IN_YEARS = 6

SCENARIOS = [
    GrowthScenario(label='optimistic',
                   cross_down_after_beginning=1.0 * YEAR,
                   stable_after_cross_down=1.0 * YEAR,
                   take_off_after_stable=1.0 * YEAR,
                   steady_after_take_off=1.0 * YEAR,
                   growth_cross_down=1.0,
                   growth_stable=1.0,
                   growth_take_off=1.0,
                   growth_steady=1.0
                   ),
    GrowthScenario(label='pessimistic',
                   cross_down_after_beginning=0.5 * YEAR,
                   stable_after_cross_down=0.5 * YEAR,
                   take_off_after_stable=3.0 * YEAR,
                   steady_after_take_off=0.5 * YEAR,
                   growth_cross_down=0.0,
                   growth_stable=1.0,
                   growth_take_off=4.0,
                   growth_steady=1.0
                   )
]


RAW_PARAMS = BaselineModelParams(timestep_in_days=DAYS_PER_TIMESTEP,
                                 days_since_start=600,  # TODO
                                 baseline_activated=True,
                                 network_power_scenario=SCENARIOS[0],  # TODO
                                 simple_mechanism=SimpleMinting(),
                                 baseline_mechanism=BaselineMinting())


PARAMS = {k: [v] for k, v in RAW_PARAMS.items()}


RAW_INITIAL_STATE = BaselineModelState(days_passed=0.0,
                                       network_power=3000,  # TODO
                                       cumm_capped_power=3000 * 2,  # TODO
                                       effective_network_time=500, # TODO
                                       reward=Reward()
                                       )

INITIAL_STATE = RAW_INITIAL_STATE


TIMESTEPS = int(ceil(SIMULATION_TIME_IN_YEARS * YEAR) / DAYS_PER_TIMESTEP)
SAMPLES = 1
