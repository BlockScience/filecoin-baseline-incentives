# %%

import plotly.express as px
from dataclasses import dataclass
from typing import Annotated
from math import log, exp


FIL = Annotated[float, "FIL"]
FILYear = Annotated[float, "FIL * Year"]
PerYear = Annotated[float, "1/year"]
Year = Annotated[float, "year"]


@dataclass
class BaselineMinting():
    initial_baseline: FIL
    issuance_baseline: FIL
    baseline_decay: float
    annual_baseline_growth: Annotated[float, "%/year"]
    gamma: float

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

    def effective_time_from_share(self,
                                  issuance_so_far: FIL) -> Year:
        return ((-1 / self.gamma)
                * log(1 - issuance_so_far / self.issuance_baseline))
