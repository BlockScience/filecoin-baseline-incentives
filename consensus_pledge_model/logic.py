from cadCAD_tools.types import Signal, VariableUpdate
from consensus_pledge_model.params import YEAR
from collections import defaultdict

from consensus_pledge_model.types import *
# TODO: Upgrade to the Consensus Pledge Model

# ## Time Tracking


def p_evolve_time(params: ConsensusPledgeParams,
                  _2,
                  _3,
                  _4) -> Signal:
    return {'delta_in_days': params['timestep_in_days']}


def s_days_passed(_1,
                  _2,
                  _3,
                  state: ConsensusPledgeDemoState,
                  signal: Signal) -> VariableUpdate:
    value = state['days_passed'] + signal['delta_in_days']
    return ('days_passed', value)


def s_delta_days(_1,
                 _2,
                 _3,
                 state: ConsensusPledgeDemoState,
                 signal: Signal) -> VariableUpdate:
    value = signal['delta_in_days']
    return ('delta_days', value)

# ## Network


def s_network_power(params: ConsensusPledgeParams,
                    _2,
                    _3,
                    state: ConsensusPledgeDemoState,
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


def s_baseline(params: ConsensusPledgeParams,
               _2,
               _3,
               state: ConsensusPledgeDemoState,
               signal: Signal) -> VariableUpdate:
    days_passed = state['days_passed']
    DAYS_TO_YEARS = 1 / 365.25
    baseline_years = days_passed * DAYS_TO_YEARS
    value = params['baseline_mechanism'].baseline_function(
        baseline_years)
    return ('baseline', value)


def s_cumm_capped_power(params: ConsensusPledgeParams,
                        _2,
                        _3,
                        state: ConsensusPledgeDemoState,
                        signal: Signal) -> VariableUpdate:
    # TODO: refactor for making it cleaner
    DAYS_TO_YEARS = 1 / YEAR
    dt = params['timestep_in_days'] * DAYS_TO_YEARS
    current_power = state['aggregate_sectors'].power_qa

    if params['baseline_activated'] is True:
        capped_power = min(current_power, state['baseline'])
    else:
        capped_power = state['baseline']

    cumm_capped_power_differential = capped_power * dt
    new_cumm_capped_power = state['cumm_capped_power'] + \
        cumm_capped_power_differential
    return ('cumm_capped_power', new_cumm_capped_power)


def s_effective_network_time(params: ConsensusPledgeParams,
                             _2,
                             history: list[list[ConsensusPledgeDemoState]],
                             state: ConsensusPledgeDemoState,
                             signal: Signal) -> VariableUpdate:
    value = params['baseline_mechanism'].effective_network_time(
        state['cumm_capped_power'])
    return ('effective_network_time', value)


def s_reward(params: ConsensusPledgeParams,
             _2,
             history: list[list[ConsensusPledgeDemoState]],
             state: ConsensusPledgeDemoState,
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
    eff_t_i = history[-1][-1]['effective_days_passed'] / 365.25  # HACK
    eff_t_f = state['effective_days_passed'] / 365.25  # HACK

    baseline_issuance_start = baseline_mechanism.issuance(eff_t_i)
    baseline_issuance_end = baseline_mechanism.issuance(eff_t_f)
    baseline_reward = baseline_issuance_end - baseline_issuance_start

    # Wrap everything together
    reward = Reward(simple_reward, baseline_reward)
    return ('reward', reward)


def s_onboarding_consensus_pledge(params, _2, _3, state, _5):
    value = None  # TODO
    return ('s_onboarding_consensus_pledge', value)


def s_onboarding_storage_pledge(params, _2, _3, state, _5):
    value = None  # TODO
    return ('onboarding_storage_pledge', value)


def s_sectors_onboard(params,
                      _2,
                      _3,
                      state: ConsensusPledgeDemoState,
                      signal: Signal) -> VariableUpdate:
    # Sector Properties
    power_rb_new = params['onboarding_rate']
    power_qa_new = power_rb_new * params['onboarding_quality_factor']
    storage_pledge = state['onboarding_storage_pledge'] * power_qa_new
    consensus_pledge = state['onboarding_consensus_pledge'] * power_rb_new
    reward_schedule = {}

    # TODO: check if copying is too shallow or deep
    current_sectors_list = state['aggregate_sectors']
    new_sectors = AggregateSector(rb_power=power_rb_new,
                                  qa_power=power_qa_new,
                                  remaining_days=params['new_sector_lifetime'],
                                  storage_pledge=storage_pledge,
                                  consensus_pledge=consensus_pledge,
                                  reward_schedule=reward_schedule)
    current_sectors_list.aggregate_sectors.append(new_sectors)

    return ('aggregate_sectors', current_sectors_list)


def s_sectors_renew(params,
                    _2,
                    _3,
                    state: ConsensusPledgeDemoState,
                    signal: Signal) -> VariableUpdate:

    renew_share = params['renewal_probability']
    # TODO: check if copying is too shallow or deep
    current_sectors_list = state['aggregate_sectors']

    power_rb_renew: PiB = 0.0
    power_qa_renew: QA_PiB = 0.0
    reward_schedule_renew = defaultdict(FIL)

    for aggregate_sector in current_sectors_list:
        # Retrieve renew values
        sector_power_rb_renew = aggregate_sector.power_rb * renew_share
        sector_power_qa_renew = aggregate_sector.power_qa * renew_share
        sector_storage_pledge_renew = aggregate_sector.storage_pledge * renew_share
        sector_consensus_pledge_renew = aggregate_sector.consensus_pledge * renew_share
        sector_schedule_renew = {k: v * renew_share
                                 for k, v
                                 in aggregate_sector.reward_schedule.items()}

        # Assign values to the new renewed sectors
        power_rb_renew += sector_power_rb_renew
        power_qa_renew += sector_power_qa_renew
        # Storage & Consensus Pledge are going to be recomputed
        # after the for-loop
        for k, v in sector_schedule_renew.items():
            reward_schedule_renew[k] += v

        # Subtract values from the non-renewed sectors
        aggregate_sector.power_rb -= sector_power_rb_renew
        aggregate_sector.power_qa -= sector_power_qa_renew
        aggregate_sector.storage_pledge -= sector_storage_pledge_renew
        aggregate_sector.consensus_pledge -= sector_consensus_pledge_renew
        for k, v in sector_schedule_renew.items():
            aggregate_sector.reward_schedule[k] -= v

    # Compute Pledges
    storage_pledge_renew = 0.0
    consensus_pledge_renew = 0.0
    storage_pledge_renew = state['onboarding_storage_pledge'] * power_qa_renew
    consensus_pledge_renew = state['onboarding_consensus_pledge'] * \
        power_qa_renew
    reward_schedule_renew = dict(reward_schedule_renew)

    # Create new sector representing the Renewed Sectors
    new_sectors = AggregateSector(rb_power=power_rb_renew,
                                  qa_power=power_qa_renew,
                                  remaining_days=params['new_sector_lifetime'],
                                  storage_pledge=storage_pledge_renew,
                                  consensus_pledge=consensus_pledge_renew,
                                  reward_schedule=reward_schedule_renew)
    current_sectors_list.aggregate_sectors.append(new_sectors)
    return ('aggregate_sectors', current_sectors_list)


def s_sectors_expire(_1,
                     _2,
                     _3,
                     state: ConsensusPledgeDemoState,
                     signal: Signal) -> VariableUpdate:
    """
    Evolve the sector lifetime & expire if they're below zero.
    Freed tokens are handled implictly when re-computing the `token_distribution
    # TODO: what happens with the locked rewards when an sector is expired?
    # FIXME: assume that locked rewards are going to be released.
    """

    current_sectors_list = state['aggregate_sectors']
    expired_sectors_indices = []

    # If remaining days are below zero, get their index for removing from the
    # active sectors list. Else, reduce their lifetime
    for i, aggregate_sector in enumerate(current_sectors_list):
        if aggregate_sector.remaining_days < 0:
            expired_sectors_indices.append(i)
        else:
            aggregate_sector.remaining_days -= state['delta_days']

    # Expire them
    for i_expired in sorted(expired_sectors_indices, reverse=True):
        current_sectors_list.pop(i_expired)
        # Implicit action: Locked Rewards & Collaterals enter Circulating Supply

    return ('aggregate_sectors', current_sectors_list)


def s_sectors_rewards(params,
                      _2,
                      _3,
                      state: ConsensusPledgeDemoState,
                      signal: Signal) -> VariableUpdate:

    # Homework for @jackhack00: Implement this SUF
    """
    Parts for what this SUF represents for each AggregateSector Schedule:
    Part 1 - Unlock Current Rewards. eg. {0: 5, 1: 10, 2: 20} -> {1: 10, 2: 20}
    NOTE: Unlocking only adds them back to circulating. Can remove item at index 0, since
    we must update at every timestep anyways, and new rewards are only added from the timestep forward
    Part 2 - Shift Reward Schedule. eg. {1: 10, 2: 20} -> {0: 10, 1: 20}
    Part 3 - Lock New Rewards. eg. {0: 10, 1: 20} -> {0: 15, 1: 25, 2: 5}

    1. Retrieve the Total Rewards during this timestep
    2. Iterate across the `AggregateSectors`
    3. Get their share of the Network QA Power: this is the % of the total reward
    due to them.
    4. For the Sector Total Reward, modify the reward schedule so that it incorporates them

    Eg. LINEAR_DURATION = 180 days means that the Total Reward should be split
    between 180 days. For 1 Timestep = 1 Day, that's 180 ts.

    Suppose LINEAR_DURATION = 3 days
    & sector_reward = 15 <=> sector_reward_per_day = 5
    & reward_schedule_init = {0: 20, 1: 30, 2: 40, 3: 50}
    then
    reward_schedule_final = {0: 20 + 5, 1: 30 + 5, 2: 40 + 5, 3: 50}

    """
    # retrieve total rewards
    total_reward = state["reward"]
    linear_duration = params["linear_duration"]
    current_sector_list = state["aggregate_sectors"]
    total_qa = state["power_qa"]
    sector_qa = state["aggregate_sectors"]
    reward_schedule = state["aggregate_sectors"]
    immediate_release = params["immediate_release_fraction"]
    days_passed = state['days_passed']

    for agg_sector in current_sector_list:
        # get share of total reward
        share_qa = sector_qa / total_qa
        available_reward = total_reward * (1.0 - immediate_release)
        share_reward = share_qa * available_reward
        daily_reward = share_reward / linear_duration
        # create new reward schedule dict to be merged
        today_reward_schedule = {
            k + days_passed: daily_reward for k in range(linear_duration)}
        # new method of transforming the dict
        new_reward_schedule = {
            k: v for k, v in reward_schedule.items() if k > days_passed}

        # create new dict, and adds the values from shifted reward schedule and
        # newly created reward schedule
        updated_reward_schedule = {x: new_reward_schedule.get(x, 0.0) + today_reward_schedule.get(x, 0.0)
                                   for x in set(new_reward_schedule).union(today_reward_schedule)}
        reward_schedule = updated_reward_schedule

    return ('aggregate_sectors', reward_schedule)  # TODO


def p_vest_fil(_1,
               _2,
               _3,
               state: ConsensusPledgeDemoState) -> VariableUpdate:
    return {}  # TODO


def p_burn_fil(_1,
               _2,
               _3,
               state: ConsensusPledgeDemoState) -> VariableUpdate:
    return {}  # TODO


def s_token_distribution(_1,
                         _2,
                         _3,
                         state: ConsensusPledgeDemoState,
                         signal: Signal) -> VariableUpdate:
    return ('token_distribution', None)  # TODO
