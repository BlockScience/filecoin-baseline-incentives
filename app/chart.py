from abc import ABC, abstractclassmethod

import altair as alt
import streamlit as st

from utils import load_constants


C = CONSTANTS = load_constants()


class AltairChart(ABC):

    X_AXIS = alt.Axis(tickMinStep=0.5)

    def __init__(self, chart, use_container_width=True):
        self.chart = st.altair_chart(chart, use_container_width=use_container_width)

    def add_rows(self, row):
        self.chart.add_rows(row)

    @abstractclassmethod
    def build(cls):
        raise NotImplementedError

    @staticmethod
    def compose_x_domain(num_steps):
        return (
            C["days_after_launch"] / C["days_per_year"],
            (C["days_after_launch"] + num_steps * C["days_per_step"]) / C["days_per_year"],
        )


class NetworkPowerAltairChart(AltairChart):
    def add_rows(self, row):
        self.chart.add_rows(row)

    @classmethod
    def build(cls, df, num_steps):
        chart = (
            alt.Chart(df)
            .mark_line(clip=True)
            .encode(
                x=alt.X(
                    "years_passed",
                    scale=alt.Scale(domain=cls.compose_x_domain(num_steps)),
                    axis=cls.X_AXIS,
                    title="Year",
                ),
                y=alt.Y(
                    "network_power",
                    scale=alt.Scale(domain=(1e4, 2e6), type="log"),
                    title="Network Power (QA PiB)",
                ),
                color="scenario",
            )
            .properties(title="Network Power vs. Time")
        )
        return cls(chart)


class MiningUtilityAltairChart(AltairChart):
    def add_rows(self, row):
        self.chart.add_rows(row)

    @classmethod
    def build(cls, df, num_steps):
        chart = (
            alt.Chart(df)
            .mark_line(clip=True)
            .encode(
                x=alt.X(
                    "years_passed",
                    scale=alt.Scale(domain=cls.compose_x_domain(num_steps)),
                    axis=cls.X_AXIS,
                    title="Year",
                ),
                y=alt.Y(
                    "mining_utility",
                    scale=alt.Scale(domain=(0.4, 2.5)),
                    title="Mining Utility (FIL / QA PiB)",
                ),
                color="scenario",
            )
            .properties(title="Mining Utility vs. Time")
        )
        return cls(chart)


class EffectiveNetworkTimeAltairChart(AltairChart):
    def add_rows(self, row):
        self.chart.add_rows(row)

    @classmethod
    def build(cls, df, num_steps):
        chart = (
            alt.Chart(df)
            .mark_line(clip=True)
            .encode(
                x=alt.X(
                    "years_passed",
                    scale=alt.Scale(domain=cls.compose_x_domain(num_steps)),
                    axis=cls.X_AXIS,
                    title="Year",
                ),
                y=alt.Y(
                    "effective_network_time",
                    scale=alt.Scale(domain=(1.5, 8)),
                    title="Effective Network Time (Years)",
                ),
                color="scenario",
            )
            .properties(title="Effective Network Time vs. Time")
        )
        return cls(chart)


class SimpleRewardAltairChart(AltairChart):
    def add_rows(self, row):
        self.chart.add_rows(row)

    @classmethod
    def build(cls, df, num_steps):
        chart = (
            alt.Chart(df)
            .mark_line(clip=True)
            .encode(
                x=alt.X(
                    "years_passed",
                    scale=alt.Scale(domain=cls.compose_x_domain(num_steps)),
                    axis=cls.X_AXIS,
                    title="Year",
                ),
                y=alt.Y(
                    "simple_reward",
                    scale=alt.Scale(domain=(0, 4e6)),
                    title="Simple Reward (FIL)",
                ),
                color="scenario",
            )
            .properties(title="Simple Reward vs. Time")
        )
        return cls(chart)


class BaselineRewardAltairChart(AltairChart):
    def add_rows(self, row):
        self.chart.add_rows(row)

    @classmethod
    def build(cls, df, num_steps):
        chart = (
            alt.Chart(df)
            .mark_line(clip=True)
            .encode(
                x=alt.X(
                    "years_passed",
                    scale=alt.Scale(domain=cls.compose_x_domain(num_steps)),
                    axis=cls.X_AXIS,
                    title="Year",
                ),
                y=alt.Y(
                    "baseline_reward",
                    scale=alt.Scale(domain=(0, 1e7)),
                    title="Baseline Reward (FIL)",
                ),
                color="scenario",
            )
            .properties(title="Baseline Reward vs. Time")
        )
        return cls(chart)
