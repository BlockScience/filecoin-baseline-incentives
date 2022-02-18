from cadCAD_tools.types import Signal, VariableUpdate
from baseline_model.params import YEAR

from baseline_model.types import BaselineModelParams, BaselineModelState, Reward, Year

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
    dt: Year = params['timestep_in_days'] / YEAR

    # Logic around the GrowthScenario object.
    if days_passed >= scenario.steady_after_beginning:
        growth_rate = scenario.growth_steady * baseline_growth
    elif days_passed >= scenario.take_off_after_beginning:
        growth_rate = scenario.growth_take_off * baseline_growth
    elif days_passed >= scenario.stabilized_after_beginning:
        growth_rate = scenario.growth_stable * baseline_growth
    else:
        growth_rate = scenario.growth_fall * baseline_growth

    fractional_growth = ((1 + growth_rate) ** dt)
    new_power = network_power * fractional_growth

    return ('network_power', new_power)


def s_baseline(params: BaselineModelParams,
               _2,
               _3,
               state: BaselineModelState,
               signal: Signal) -> VariableUpdate:
    days_passed = state['days_passed']
    DAYS_TO_YEARS = 1 / 365.25
    baseline_years = days_passed * DAYS_TO_YEARS
    value = params['baseline_mechanism'].baseline_function(
        baseline_years)
    return ('baseline', value)


def s_cumm_capped_power(params: BaselineModelParams,
                        _2,
                        _3,
                        state: BaselineModelState,
                        signal: Signal) -> VariableUpdate:
    # TODO: refactor for making it cleaner
    DAYS_TO_YEARS = 1 / YEAR
    dt = params['timestep_in_days'] * DAYS_TO_YEARS
    current_power = state['network_power']
    capped_power = min(current_power, state['baseline'])
    cumm_capped_power_differential = capped_power * dt
    new_cumm_capped_power = state['cumm_capped_power'] + \
        cumm_capped_power_differential
    return ('cumm_capped_power', new_cumm_capped_power)


def s_effective_network_time(params: BaselineModelParams,
                             _2,
                             history: list[list[BaselineModelState]],
                             state: BaselineModelState,
                             signal: Signal) -> VariableUpdate:
    if params['baseline_activated'] is True:
        value = params['baseline_mechanism'].effective_network_time(
            state['cumm_capped_power'])
    else:
        # If deactivated, make the ENT run on the same rate of the physical time
        value = state['effective_network_time'] + state['delta_days'] / YEAR
    return ('effective_network_time', value)


def s_reward(params: BaselineModelParams,
             _2,
             history: list[list[BaselineModelState]],
             state: BaselineModelState,
             signal: Signal) -> VariableUpdate:
    # Simple Minting
    simple_mechanism = params['simple_mechanism']
    t_i = history[-1][-1]['days_passed'] / YEAR
    t_f = state['days_passed'] / YEAR

    simple_issuance_start = simple_mechanism.issuance(t_i)
    simple_issuance_end = simple_mechanism.issuance(t_f)
    simple_reward = simple_issuance_end - simple_issuance_start

    # Baseline Minting
    baseline_mechanism = params['baseline_mechanism']
    eff_t_i = history[-1][-1]['effective_network_time']
    eff_t_f = state['effective_network_time']

    baseline_issuance_start = baseline_mechanism.issuance(eff_t_i)
    baseline_issuance_end = baseline_mechanism.issuance(eff_t_f)
    baseline_reward = baseline_issuance_end - baseline_issuance_start

    # Wrap everything together
    reward = Reward(simple_reward, baseline_reward)
    return ('reward', reward)
