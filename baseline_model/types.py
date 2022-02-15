from typing import Annotated, TypedDict


Days = Annotated[float, 'days']

class BaselineModelParams (TypedDict):
    timestep_in_days: Days

class BaselineModelState (TypedDict):
    days_passed: Days