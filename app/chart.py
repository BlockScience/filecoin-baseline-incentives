from abc import ABC, abstractclassmethod

import altair as alt
import streamlit as st


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
                    scale=alt.Scale(domain=(0, (num_steps - 1) / 4)),
                    axis=alt.Axis(tickMinStep=0.25),
                    title="Year",
                ),
                y=alt.Y(
                    "consensus_power_in_zib",
                    scale=alt.Scale(domain=(0, 100)),
                    title="Network Power (ZiB)",
                ),
                color="scenario",
            )
            .properties(title="Network Power (ZiB) Over Time")
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
                    scale=alt.Scale(domain=(0, (num_steps - 1) / 4)),
                    axis=alt.Axis(tickMinStep=0.25),
                    title="Year",
                ),
                y=alt.Y(
                    "utility",
                    scale=alt.Scale(domain=(0, 100)),
                    title="Mining Utility (Reward per Power)",
                ),
                color="scenario",
            )
            .properties(title="Mining Utility Over Time")
        )
        return cls(chart)
