from cadCAD_tools.types import Signal, VariableUpdate

from baseline_model.types import BaselineModelParams, BaselineModelState, Year

# ## Time Tracking


def p_evolve_time(params: BaselineModelParams,
                  _2,
                  _3,
                  _4) -> Signal:
    return {'delta_in_days': params['timestep_in_days']}


def s_days_passed(_1,
                  _2,
                  _3,
                  state: BaselineModelState,
                  signal: Signal) -> VariableUpdate:
    value = state['days_passed'] + signal['delta_in_days']
    return ('days_passed', value)


def s_delta_days(_1,
                 _2,
                 _3,
                 state: BaselineModelState,
                 signal: Signal) -> VariableUpdate:
    value = signal['delta_in_days']
    return ('delta_days', value)

# ## Network


def s_network_power(params: BaselineModelParams,
                    _2,
                    _3,
                    state: BaselineModelState,
                    signal: Signal) -> VariableUpdate:

    network_power = state['network_power']
    days_passed = state['days_passed']
    baseline_growth = params['baseline_mechanism'].annual_baseline_growth
    scenario = params['network_power_scenario']

    dt: Year = params['timestep_in_days'] / 365.25

    if days_passed >= scenario.steady_after_beginning:
        growth_rate = scenario.growth_steady * baseline_growth
    elif days_passed >= scenario.take_off_after_beginning:
        growth_rate = scenario.growth_take_off * baseline_growth
    elif days_passed >= scenario.stabilized_after_beginning:
        growth_rate = scenario.growth_stable * baseline_growth
    else:
        growth_rate = scenario.growth_cross_down * baseline_growth

    fractional_growth = ((1 + growth_rate) ** dt)
    new_power = network_power * fractional_growth

    return ('network_power', new_power)


def p_baseline_function(params: BaselineModelParams,
                        _2,
                        _3,
                        state: BaselineModelState) -> Signal:
    return {}


def s_cumm_capped_power(params: BaselineModelParams,
                        _2,
                        _3,
                        state: BaselineModelState,
                        signal: Signal) -> VariableUpdate:
    # TODO: refactor for making it cleaner
    DAYS_TO_YEARS = 1 / 365.25
    dt = params['timestep_in_days'] * DAYS_TO_YEARS
    days_passed = state['days_passed']
    baseline_years = (days_passed + params['days_since_start']) * DAYS_TO_YEARS
    current_power = state['network_power']
    current_baseline = params['baseline_mechanism'].baseline_function(baseline_years)
    capped_power = min(current_power, current_baseline)
    cumm_capped_power_differential = capped_power * dt
    new_cumm_capped_power = state['cumm_capped_power'] + cumm_capped_power_differential
    return ('cumm_capped_power', new_cumm_capped_power)
