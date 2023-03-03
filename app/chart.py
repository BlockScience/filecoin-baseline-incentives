from abc import ABC, abstractclassmethod

import plotly.express as px
import streamlit as st

from utils import load_constants


C = CONSTANTS = load_constants()


class PlotlyChart(ABC):
    def __init__(self, chart, use_container_width=True):
        self.chart = st.plotly_chart(chart, use_container_width=use_container_width)

    @abstractclassmethod
    def build(cls):
        raise NotImplementedError

    @staticmethod
    def compose_x_domain(num_steps):
        return (
            C["days_after_launch"] / C["days_per_year"],
            (C["days_after_launch"] + num_steps * C["days_per_step"]) / C["days_per_year"],
        )


class NetworkPowerPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps):
        chart = px.line(
            df,
            x="years_passed",
            y="power_rb",
            color="scenario",
            title="RB Network Power vs. Time",
            labels={
                "years_passed": "Year",
                "network_power": "Raw Bytes Network Power (RB PiB)",
            },
            range_x=cls.compose_x_domain(num_steps),
            range_y=(1e4, 2e6),
            log_y=True,
        )
        return cls(chart)


class MiningUtilityPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps):
        chart = px.line(
            df,
            x="years_passed",
            y="mining_utility",
            color="scenario",
            title="Mining Utility vs. Time",
            labels={
                "years_passed": "Year",
                "mining_utility": "Mining Utility (% of baseline scenario)",
            },
            range_x=cls.compose_x_domain(num_steps),
            range_y=(0.4, 2.5),
        )
        return cls(chart)


class EffectiveNetworkTimePlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps):
        chart = px.line(
            df,
            x="years_passed",
            y="effective_network_time",
            color="scenario",
            title="Effective Network Time vs. Time",
            labels={
                "years_passed": "Year",
                "effective_network_time": "Effective Network Time (Years)",
            },
            range_x=cls.compose_x_domain(num_steps),
            range_y=(1.5, 8),
        )
        return cls(chart)


class SimpleRewardPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps):
        chart = px.line(
            df,
            x="years_passed",
            y="simple_reward",
            color="scenario",
            title="Simple Reward vs. Time",
            labels={
                "years_passed": "Year",
                "simple_reward": "Simple Reward (FIL / month)",
            },
            range_x=cls.compose_x_domain(num_steps),
            range_y=(1e6, 3e6),
        )
        return cls(chart)


class BaselineRewardPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps):
        chart = px.line(
            df,
            x="years_passed",
            y="baseline_reward",
            color="scenario",
            title="Baseline Reward vs. Time",
            labels={
                "years_passed": "Year",
                "baseline_reward": "Baseline Reward (FIL / month)",
            },
            range_x=cls.compose_x_domain(num_steps),
            range_y=(1e6, 7e6),
        )
        return cls(chart)


class MarginalRewardPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps):
        chart = px.line(
            df,
            x="years_passed",
            y="marginal_reward",
            color="scenario",
            title="Marginal Reward vs. Time",
            labels={
                "years_passed": "Year",
                "marginal_reward": "Marginal Reward (FIL / (month * RB PiB))",
            },
            range_x=cls.compose_x_domain(num_steps),
            range_y=(0, 1e3),
            # log_y=True
        )
        return cls(chart)
