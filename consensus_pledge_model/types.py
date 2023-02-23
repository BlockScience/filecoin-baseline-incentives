from typing import Annotated, TypedDict, Union
from math import exp, log, nan
from dataclasses import dataclass

# TODO: Upgrade to the Consensus Pledge Model

# Units
Days = Annotated[float, 'days']
FIL = Annotated[float, "FIL"]
FILYear = Annotated[float, "FIL * Year"] # TODO: check if this is right
PerYear = Annotated[float, "1/year"]
Year = Annotated[float, "year"]
PiB = Annotated[float, "PiB (QA)"]
QA_PiB = Annotated[float, "PiB (QA)"]
PiB_per_Day = Annotated[float, "PiB per Day"]
FIL_per_QA_PiB = Annotated[float, "PiB per Day"]

@dataclass
class GrowthScenario():
    """
    Container for wrapping all the parameters for a growth scenario.
    """
    label: str = 'no-label'

    fall_after_beginning: Annotated[float, 'days'] = 365.25
    stable_after_fall: Annotated[float, 'days'] = 365.25
    take_off_after_stable: Annotated[float, 'days'] = 365.25
    steady_after_take_off: Annotated[float, 'days'] = 365.25

    # Growth ratio as a fraction of the baseline function growth
    growth_fall: Annotated[float, '%/baseline'] = 1.0
    growth_stable: Annotated[float, '%/baseline'] = 1.0
    growth_take_off: Annotated[float, '%/baseline'] = 1.0
    growth_steady: Annotated[float, '%/baseline'] = 1.0

    @property
    def stabilized_after_beginning(self):
        return self.stable_after_fall + self.fall_after_beginning

    @property
    def take_off_after_beginning(self):
        return self.stabilized_after_beginning + self.take_off_after_stable
    
    @property
    def steady_after_beginning(self):
        return self.take_off_after_beginning + self.steady_after_take_off



@dataclass
class Reward():
    simple_reward: FIL = nan
    baseline_reward: FIL = nan

    @property
    def block_reward(self):
        return self.simple_reward + self.baseline_reward


@dataclass
class SimpleMinting():
    total_issuance: FIL = 0.33e9
    decay = log(2) / 6.0

    def issuance(self, years_passed: Year) -> FIL:
        issuance_fraction = (1 - exp(-1 * self.decay * years_passed))
        return self.total_issuance * issuance_fraction

    
@dataclass
class BaselineMinting(SimpleMinting):
    # Parameters
    total_issuance: FIL = 0.77e9
    decay: float = log(2) / 6.0
    initial_baseline: FIL = 2888
    annual_baseline_growth: Annotated[float, "%/year"] = 1.0
    # gamma: float = 0.0 # TODO

    @property
    def log_baseline_growth(self) -> PerYear:
        return log(1 + self.annual_baseline_growth)

    def effective_network_time(self,
                               cumm_capped_power: FILYear) -> Year:
        g = self.log_baseline_growth
        inner_term = (g * cumm_capped_power / self.initial_baseline)
        return log(1 + inner_term) / g

    def baseline_function(self,
                          years_passed: Year) -> FIL:
        return (self.initial_baseline
                * (1 + self.annual_baseline_growth)
                ** years_passed)

    def issuance(self, effective_years_passed: Year) -> FIL:
        issuance_fraction = (1 - exp(-1 * self.decay * effective_years_passed))
        return self.total_issuance * issuance_fraction

    # def effective_time_from_share(self,
    #                               issuance_so_far: FIL) -> Year:
    #     return ((-1 / self.gamma)
    #             * log(1 - issuance_so_far / self.issuance_baseline))


class BaselineModelParams (TypedDict):
    timestep_in_days: Days
    baseline_activated: bool
    network_power_scenario: GrowthScenario
    simple_mechanism: SimpleMinting
    baseline_mechanism: BaselineMinting
    
class BaselineModelSweepParams (TypedDict):
    timestep_in_days: list[Days]
    baseline_activated: list[bool]
    network_power_scenario: list[GrowthScenario]
    simple_mechanism: list[SimpleMinting]
    baseline_mechanism: list[BaselineMinting]
    
# TODO: deactivate
class BaselineModelState (TypedDict):
    days_passed: Days
    delta_days: Days
    network_power: QA_PiB
    baseline: QA_PiB
    cumm_capped_power: FILYear
    effective_network_time: Year
    reward: Reward
    
@dataclass
class AggregateSector():
    power_rb: PiB
    power_qa: QA_PiB
    remaining_days: Days
    storage_pledge: FIL
    consensus_pledge: FIL
    # Key indicates Simulation Day on which Value is going to the Circ. Supply
    reward_schedule: dict[Days, FIL]
    
    @property
    def collateral(self) -> FIL:
        return self.storage_pledge + self.consensus_pledge

    @property
    def locked_rewards(self) -> FIL:
        return sum(self.reward_schedule.values())

    @property
    def locked(self) -> FIL:
        return self.collateral + self.locked_rewards


@dataclass
class TokenDistribution():
    minted: float
    vested: float
    collateral: float
    locked_rewards: float
    burnt: float

    def update_distribution(self, 
                            new_vested: float,
                            minted: float,
                            aggregate_sectors: list[AggregateSector],
                            marginal_burn: float = 0.0):
        self.minted = minted
        self.vested += new_vested
        self.collateral = sum(el.collateral for el in aggregate_sectors)
        self.locked_rewards = sum(el.locked_rewards for el in aggregate_sectors)
        self.burnt += marginal_burn
        return self


    @property
    def locked(self) -> FIL:
        return self.locked_rewards + self.collateral

    @property
    def available(self) -> FIL:
        return self.minted + self.vested - self.burnt

    @property
    def circulating(self) -> FIL:
        return self.available - self.locked


@dataclass
class AggregateSectorList():
    aggregate_sectors: list[AggregateSector]

    @property
    def power_qa(self) -> QA_PiB:
        return sum(agg_sector.power_qa for agg_sector in self.aggregate_sectors)

class ConsensusPledgeDemoState(TypedDict):
    days_passed: Days
    delta_days: Days
    aggregate_sectors: list[AggregateSector]
    token_distribution: TokenDistribution
    power_qa: QA_PiB
    power_rb: PiB
    baseline: PiB
    cumm_capped_power: FILYear
    effective_days_passed: Days
    reward: Reward
    storage_pledge_per_new_qa_power: FIL_per_QA_PiB
    consensus_pledge_per_new_qa_power: FIL_per_QA_PiB


class ConsensusPledgeParams(TypedDict):
    timestep_in_days: Days
    vesting_schedule: dict[Days, FIL] # Days = Days since Simulation Start
    # Collateral Params
    target_locked_supply: float
    storage_pledge_factor: Days
    # Minting Params
    simple_mechanism: object # TODO: re-evaluate it
    baseline_mechanism: object # TODO: re-evaluate it
    baseline_activated: bool
    # Reward Schedule Params
    linear_duration: Days
    immediate_release_fraction: float
    # Behavioral Params   
    new_sector_lifetime: Days
    onboarding_rate: PiB_per_Day
    onboarding_quality_factor: float
    renewal_probability: float


    