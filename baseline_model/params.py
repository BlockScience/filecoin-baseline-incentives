from baseline_model.types import BaselineMinting, BaselineModelState, BaselineModelParams, NetworkPowerScenario

YEAR = 365.25
SCENARIOS = [
    NetworkPowerScenario(label='optimistic',
                         cross_down_after_beginning=1.0 * YEAR,
                         stable_after_cross_down=1.0 * YEAR,
                         take_off_after_stable=1.0 * YEAR,
                         steady_after_take_off=1.0 * YEAR,
                         growth_cross_down=1.0,
                         growth_stable=1.0,
                         growth_take_off=1.0,
                         growth_steady=1.0
                         ),
    NetworkPowerScenario(label='pessimistic',
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


PARAMS = BaselineModelParams(timestep_in_days=15.0,
                             days_since_start=600,  # TODO
                             baseline_activated=True,
                             network_power_scenario=SCENARIOS[0],  # TODO
                             baseline_mechanism=BaselineMinting())


INITIAL_STATE = BaselineModelState(days_passed=0.0,
                                   network_power=3000,  # TODO
                                   cumm_capped_power=3000 * 2  # TODO
                                   )
