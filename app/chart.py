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
            y=["power_rb", "baseline"],
            title="RB Network Power vs. Time",
            labels={
                "years_passed": "Year",
                "network_power": "Raw Bytes Network Power (RB PiB)",
            },
            range_x=cls.compose_x_domain(num_steps),
            range_y=(10_000, 50_000),
            #log_y=True,
        )
        return cls(chart)

class QAPowerPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps):
        chart = px.line(
            df,
            x="years_passed",
            y='power_qa',
            title="QA Power vs. Time",
            labels={
                "years_passed": "Year",
                "network_power": "QA Network Power (QA PiB)",
            },
            range_x=cls.compose_x_domain(num_steps),
            range_y=(10_000, 150_000),
            #log_y=True,
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
            range_y=(2.5, 4.5),
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
            range_y=(60_000, 100_000),
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
            range_y=(50_000, 150_000),
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
            range_y=(0, 12),
            # log_y=True
        )
        return cls(chart)


class TokenDistributionPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps):
        chart = px.line(
            df,
            x="years_passed",
            y=["fil_circulating", "fil_locked_reward", "fil_collateral", "fil_vested", 'fil_locked'],
            title="Token Distribution",
            line_dash='scenario',
            labels={
                "years_passed": "Year"
            },
            range_x=cls.compose_x_domain(num_steps),
            range_y=(0, 500_000_000),
            #log_y=True,
        )
        return cls(chart)
    

class CriticalCostPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps):
        chart = px.line(
            df,
            x="years_passed",
            y="critical_cost",
            title="Critical Cost",
            line_dash='scenario',
            labels={
                "years_passed": "Year"
            },
            range_x=cls.compose_x_domain(num_steps),
            range_y=(0, 40_000_000),
            #log_y=True,
        )
        return cls(chart)
    

class CirculatingSurplusPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps):
        chart = px.line(
            df,
            x="years_passed",
            y="circulating_surplus",
            title="Circulating Surplus",
            line_dash='scenario',
            labels={
                "years_passed": "Year"
            },
            range_x=cls.compose_x_domain(num_steps),
            range_y=(5, 30),
        )
        return cls(chart)
    
class OnboardingCollateralPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps):
        chart = px.line(
            df,
            x="years_passed",
            y="consensus_pledge_per_new_qa_power",
            title="Initial Pledge per QA-PiB",
            labels={
                "years_passed": "Year"
            },
            range_x=cls.compose_x_domain(num_steps),
            range_y=(0, 6_000),
        )
        return cls(chart)