from typing import Annotated, TypedDict
from math import exp, log, nan
from dataclasses import dataclass

# Units
Days = Annotated[float, 'days']
FIL = Annotated[float, "FIL"]
FILYear = Annotated[float, "FIL * Year"]
PerYear = Annotated[float, "1/year"]
Year = Annotated[float, "year"]
QA_PiB = Annotated[float, "PiB (QA)"]

@dataclass
class GrowthScenario():
    label: str

    cross_down_after_beginning: Annotated[float, 'days']
    stable_after_cross_down: Annotated[float, 'days']
    take_off_after_stable: Annotated[float, 'days']
    steady_after_take_off: Annotated[float, 'days']

    growth_cross_down: Annotated[float, '%/baseline']
    growth_stable: Annotated[float, '%/baseline']
    growth_take_off: Annotated[float, '%/baseline']
    growth_steady: Annotated[float, '%/baseline']

    @property
    def stabilized_after_beginning(self):
        return self.stable_after_cross_down + self.cross_down_after_beginning

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
    total_issuance: FIL = 0.9e9 # TODO: check
    decay = log(2) / 6.0 # TODO: check

    def issuance(self, years_passed: Year) -> FIL:
        issuance_fraction = (1 - exp(-1 * self.decay * years_passed))
        return self.total_issuance * issuance_fraction

    
@dataclass
class BaselineMinting(SimpleMinting):
    # Parameters
    total_issuance: FIL = 1.1e9
    decay: float = log(2) / 6.0 # TODO: check
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
    days_since_start: Days
    baseline_activated: bool
    network_power_scenario: GrowthScenario
    simple_mechanism: SimpleMinting
    baseline_mechanism: BaselineMinting
    
class BaselineModelState (TypedDict):
    days_passed: Days
    delta_days: Days
    network_power: QA_PiB
    baseline: QA_PiB
    cumm_capped_power: FILYear
    effective_network_time: Year
    reward: Reward
    