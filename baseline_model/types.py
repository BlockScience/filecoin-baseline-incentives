from typing import Annotated, TypedDict
from math import exp, log
from dataclasses import dataclass

# Units
Days = Annotated[float, 'days']
FIL = Annotated[float, "FIL"]
FILYear = Annotated[float, "FIL * Year"]
PerYear = Annotated[float, "1/year"]
Year = Annotated[float, "year"]
QA_PiB = Annotated[float, "PiB (QA)"]

@dataclass
class NetworkPowerScenario():
    label: str

    cross_down_after_beginning: Annotated[float, 'days']
    stable_after_cross_down: Annotated[float, 'days']
    take_off_after_cross_down: Annotated[float, 'days']
    steady_after_take_off: Annotated[float, 'days']

    growth_initial: Annotated[float, '%/baseline']
    growth_cross_down: Annotated[float, '%/baseline']
    growth_stable: Annotated[float, '%/baseline']
    growth_take_off: Annotated[float, '%/baseline']
    growth_steady: Annotated[float, '%/baseline']

    @property
    def stabilized_after_beginning(self):
        return self.stable_after_cross_down + self.cross_down_after_beginning

    @property
    def take_off_after_beginning(self):
        return self.cross_down_after_beginning + self.take_off_after_cross_down
    
    @property
    def steady_after_beginning(self):
        return self.take_off_after_beginning + self.steady_after_take_off


    
@dataclass
class BaselineMinting():
    # Parameters
    initial_baseline: FIL = 2888
    issuance_baseline: FIL = 1.1e9
    baseline_decay: float = log(2) / 6.0
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

    def baseline_issuance(self,
                          effective_years_passed: Year) -> FIL:
        return self.issuance_baseline * (1 - exp(-1 *
                                                 self.baseline_decay *
                                                 effective_years_passed))

    # def effective_time_from_share(self,
    #                               issuance_so_far: FIL) -> Year:
    #     return ((-1 / self.gamma)
    #             * log(1 - issuance_so_far / self.issuance_baseline))


class BaselineModelParams (TypedDict):
    timestep_in_days: Days
    days_since_start: Days
    baseline_activated: bool
    network_power_scenario: NetworkPowerScenario
    
class BaselineModelState (TypedDict):
    days_passed: Days
    network_power: QA_PiB
    baseline_mechanism: BaselineMinting
    cumm_capped_power: FILYear
    