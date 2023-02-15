from consensus_pledge_model.logic import s_network_power
from consensus_pledge_model.types import BaselineMinting, NetworkPowerScenario
from pytest import approx


def test_scenario():

    # Test 1, early growth
    state = dict(network_power=100, days_passed=0.0)
    params = dict(baseline_mechanism=BaselineMinting(),
                  timestep_in_days=5,
                  network_power_scenario=NetworkPowerScenario(None,
                                                              10, 20, 30, 40,
                                                              1.0, 1.2, 1.4, 1.6)
                  )

    output = s_network_power(params, None, None, state, None)
    assert output[0] == 'network_power'
    assert type(output[1]) == float
    assert output[1] == approx(100 * (1 + (1.0 * 1.0)) ** (5 / 365.25))

    # Test 2, late growth
    state = dict(network_power=100, days_passed=1000.0)
    params = dict(baseline_mechanism=BaselineMinting(),
                  timestep_in_days=365.25,
                  network_power_scenario=NetworkPowerScenario(None,
                                                              10, 20, 30, 40,
                                                              1.0, 1.2, 1.4, 1.6)
                  )

    output = s_network_power(params, None, None, state, None)
    assert output[0] == 'network_power'
    assert type(output[1]) == float
    assert output[1] == approx(100 * (1 + (1.0 * 1.6)) ** (365.25 / 365.25))


    # Test 3, intermediate growth
    state = dict(network_power=100, days_passed=25.0)
    params = dict(baseline_mechanism=BaselineMinting(),
                  timestep_in_days=5,
                  network_power_scenario=NetworkPowerScenario(None,
                                                              10, 20, 30, 40,
                                                              1.0, 1.2, 1.4, 1.6)
                  )

    output = s_network_power(params, None, None, state, None)
    assert output[0] == 'network_power'
    assert type(output[1]) == float
    assert output[1] == approx(100 * (1 + (1.0 * 1.4)) ** (5 / 365.25))

