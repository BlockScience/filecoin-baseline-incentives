from cadCAD_tools.types import Signal, VariableUpdate

from baseline_model.types import BaselineModelParams, BaselineModelState

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

def p_evolve_network(params: BaselineModelParams,
                        _2,
                        _3,
                        state: BaselineModelState) -> Signal:
    pass


def s_baseline_function(params: BaselineModelParams,
                        _2,
                        _3,
                        state: BaselineModelState,
                        signal: Signal) -> VariableUpdate:
    pass


def s_network_power(params: BaselineModelParams,
                    _2,
                    _3,
                    state: BaselineModelState,
                    signal: Signal) -> VariableUpdate:
    pass
