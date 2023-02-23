from cadCAD_tools.types import Signal, VariableUpdate
from consensus_pledge_model.params import YEAR
from collections import defaultdict

from consensus_pledge_model.types import *

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


def s_power_qa(params: ConsensusPledgeParams,
               _2,
               _3,
               state: ConsensusPledgeDemoState,
               signal: Signal) -> VariableUpdate:
    value = sum(s.power_qa for s in state['aggregate_sectors'])
    return ('power_qa', value)


def s_power_rb(params: ConsensusPledgeParams,
               _2,
               _3,
               state: ConsensusPledgeDemoState,
               signal: Signal) -> VariableUpdate:
    value = sum(s.power_rb for s in state['aggregate_sectors'])
    return ('power_rb', value)


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
    current_power = state['power_qa']

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


def s_consensus_pledge_per_new_qa_power(params,
                                        _2,
                                        _3,
                                        state,
                                        _5):
    """
    CP per Sector = TLS * CircSupply * SectorQAP / max(baseline, QA_Net_Power)
    Sum[SectorQAP] = OnboardingNetworkQAP
    CP this round = OnboardingNetworkQAP * 
    What should be returned: TLS * CircSupply / max(baseline, CurrentNetworkQAP)
    """
    value = params['target_locked_supply']
    value *= state['token_distribution'].circulating
    value /= max(state['baseline'], state['power_qa'])
    return ('consensus_pledge_per_new_qa_power', value)


def s_storage_pledge_per_new_qa_power(params,
                                      _2,
                                      history: dict[list, dict[list, ConsensusPledgeDemoState]],
                                      state: ConsensusPledgeDemoState, _5):
    """
    SP per Sector = Estimated 20 days of daily BR for the Sector
    SP this round = OnboardingNetworkQAP * 20 * DailyBR / ExistingNetworkQAP
    What should be returned: 20 * DailyBR / CurrentNetworkQAP
    """

    current_reward = state["reward"].block_reward
    dt = state['delta_days']
    daily_reward_estimate = current_reward / dt

    value = daily_reward_estimate
    value *= 20
    value /= state["power_qa"]

    #total_reward = state["reward"].block_reward
    #total_qa = state["power_qa"]
    #multiplier_days = 20
    #value = multiplier_days * total_reward / total_qa
    return ('storage_pledge_per_new_qa_power', value)


def s_sectors_onboard(params,
                      _2,
                      _3,
                      state: ConsensusPledgeDemoState,
                      signal: Signal) -> VariableUpdate:
    # Sector Properties
    power_rb_new = params['onboarding_rate']
    power_qa_new = power_rb_new * params['onboarding_quality_factor']
    storage_pledge = state['storage_pledge_per_new_qa_power'] * power_qa_new
    consensus_pledge = state['consensus_pledge_per_new_qa_power'] * power_qa_new
    reward_schedule = {}

    # TODO: check if copying is too shallow or deep (low priority)
    current_sectors_list = state['aggregate_sectors']
    new_sectors = AggregateSector(power_rb=power_rb_new,
                                  power_qa=power_qa_new,
                                  remaining_days=params['new_sector_lifetime'],
                                  storage_pledge=storage_pledge,
                                  consensus_pledge=consensus_pledge,
                                  reward_schedule=reward_schedule)
    current_sectors_list.append(new_sectors)

    return ('aggregate_sectors', current_sectors_list)


def s_sectors_renew(params,
                    _2,
                    _3,
                    state: ConsensusPledgeDemoState,
                    signal: Signal) -> VariableUpdate:

    renew_share = params['renewal_probability']
    # TODO: check if copying is too shallow or deep (low priority)
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

    storage_pledge_renew = state['storage_pledge_per_new_qa_power']
    storage_pledge_renew *= power_qa_renew

    consensus_pledge_renew = state['consensus_pledge_per_new_qa_power']
    consensus_pledge_renew *= power_qa_renew

    reward_schedule_renew = dict(reward_schedule_renew)

    # Create new sector representing the Renewed Sectors
    new_sectors = AggregateSector(power_rb=power_rb_renew,
                                  power_qa=power_qa_renew,
                                  remaining_days=params['new_sector_lifetime'],
                                  storage_pledge=storage_pledge_renew,
                                  consensus_pledge=consensus_pledge_renew,
                                  reward_schedule=reward_schedule_renew)
    current_sectors_list.append(new_sectors)
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


def s_sectors_rewards(params: ConsensusPledgeParams,
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
    total_reward = state["reward"].block_reward
    linear_duration = params["linear_duration"]
    current_sector_list = state["aggregate_sectors"]
    total_qa = state["power_qa"]
    immediate_release = params["immediate_release_fraction"]
    days_passed = state['days_passed']

    for agg_sector in current_sector_list:
        reward_schedule = agg_sector.reward_schedule
        # get share of total reward
        sector_qa = agg_sector.power_qa
        share_qa = sector_qa / total_qa
        available_reward = total_reward * (1.0 - immediate_release)
        share_reward = share_qa * available_reward
        daily_reward = share_reward / linear_duration
        # create new reward schedule dict to be merged
        today_reward_schedule = {k + days_passed: daily_reward
                                 for k
                                 in range(linear_duration)}
        # new method of transforming the dict
        new_reward_schedule = {k: v
                               for k, v
                               in reward_schedule.items() if k > days_passed}

        # create new dict, and adds the values from shifted reward schedule and
        # newly created reward schedule
        reward_days = set(new_reward_schedule | today_reward_schedule)
        updated_reward_schedule = {unlock_day: new_reward_schedule.get(
            unlock_day, 0.0) + today_reward_schedule.get(unlock_day, 0.0)
            for unlock_day
            in reward_days}

        agg_sector.reward_schedule = updated_reward_schedule

    return ('aggregate_sectors', current_sector_list)


def p_vest_fil(params: ConsensusPledgeParams,
               _2,
               _3,
               state: ConsensusPledgeDemoState) -> VariableUpdate:
    now = state['days_passed']
    value = params['vesting_schedule'].get(now, 0.0)
    return {'fil_to_vest': value}


def p_burn_fil(_1,
               _2,
               _3,
               state: ConsensusPledgeDemoState) -> VariableUpdate:
    return {'fil_to_burn': 0.0}


def s_token_distribution(params: ConsensusPledgeParams,
                         _2,
                         _3,
                         state: ConsensusPledgeDemoState,
                         signal: Signal) -> VariableUpdate:
    distribution = state["token_distribution"]
    rewards = state["reward"].block_reward
    aggregate_sectors = state["aggregate_sectors"]
    burn = signal.get('fil_to_burn', 0.0)
    today_vested = signal.get("fil_to_vest", 0.0)

    distribution = distribution.update_distribution(
        new_rewards=rewards,
        new_vested=today_vested,
        aggregate_sectors=aggregate_sectors,
        marginal_burn=burn)

    return ('token_distribution', distribution)
