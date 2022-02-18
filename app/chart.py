from abc import ABC, abstractclassmethod

import altair as alt
import streamlit as st

from utils import load_constants


C = CONSTANTS = load_constants()


class AltairChart(ABC):
    def __init__(self, chart, use_container_width=True):
        self.chart = st.altair_chart(chart, use_container_width=use_container_width)

    def add_rows(self, row):
        self.chart.add_rows(row)

    @abstractclassmethod
    def build(cls):
        raise NotImplementedError


class NetworkPowerAltairChart(AltairChart):
    def add_rows(self, row):
        self.chart.add_rows(row)

    @classmethod
    def build(cls, df, num_steps):
        chart = (
            alt.Chart(df)
            .mark_line()
            .encode(
                x=alt.X(
                    "years_passed",
                    scale=alt.Scale(domain=(
                        C['days_after_launch'] / C['days_per_year'],
                        (C['days_after_launch'] + num_steps * C['days_per_step']) / C['days_per_year']
                    )),
                    axis=alt.Axis(tickMinStep=.5),
                    title="Year",
                ),
                y=alt.Y(
                    "network_power",
                    scale=alt.Scale(domain=(1e4, 1e6)),
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
            .mark_line()
            .encode(
                x=alt.X(
                    "years_passed",
                    scale=alt.Scale(domain=(
                        C['days_after_launch'] / C['days_per_year'],
                        (C['days_after_launch'] + num_steps * C['days_per_step']) / C['days_per_year']
                    )),
                    axis=alt.Axis(tickMinStep=.5),
                    title="Year",
                ),
                y=alt.Y(
                    "mining_utility",
                    scale=alt.Scale(domain=(0, 10), clamp=True),
                    title="Mining Utility (FIL / QA PiB)",
                ),
                color="scenario",
            )
            .properties(title="Mining Utility Over Time")
        )
        return cls(chart)
