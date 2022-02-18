from collections import OrderedDict
import os
import time
import pandas as pd
import streamlit as st

from chart import NetworkPowerAltairChart, MiningUtilityAltairChart
from description import description
from glossary import glossary
from model import run_cadcad_model
from stats import stat2meta
from utils import load_constants


C = CONSTANTS = load_constants()


# Define layout

st.set_page_config(layout="wide")

_, image_container, _ = st.columns([1,4,1])

with image_container:
    st.image(os.path.join(os.path.dirname(__file__), "assets", "logo.png"), width=800)

st.markdown("# Description")
with st.expander("See description"):
    description()

st.markdown("# Stats")
stats_dboard = st.empty()

st.markdown("# Graphs")
plot_container = st.container()

st.markdown("# Conclusions")
conclusions_container = st.container()

st.markdown("# Glossary")
glossary_container = st.container()
with glossary_container:
    with st.expander("See glossary"):
        glossary()

st.markdown("# Download")
download_container = st.container()

# Define sidebar

st.sidebar.markdown("# Simulator")

run_simulation = st.sidebar.button("Run")

st.sidebar.markdown("## Progress")

progress_bar = st.sidebar.progress(0)
progress_text = st.sidebar.text("0.0% Complete")

st.sidebar.markdown("## Network Power Parameters")

defaults = C["network_power"]["pessimistic"]

st.sidebar.text("""
The network power changes course.

For each change, we ask:

- When? (Years Since Prev. Change)
- How fast? (Frac. BaseFunc Growth)
""")

st.sidebar.markdown("### 1️⃣ Cross BaseFunc From Above")

fall_after_beginning = (
    st.sidebar.slider(
        "When?", 0., 8., defaults["fall_after_beginning"] / C['days_per_year'], .25, key='fall'
    ) * C['days_per_year']
) + C['days_after_launch']

growth_fall = st.sidebar.slider(
    "How fast?", -.2, 1.2, defaults["growth_fall"], .1, key='fall'
)

st.sidebar.markdown("### 2️⃣ Stabilize Below BaseFunc")

stable_after_fall = st.sidebar.slider(
    "When?", 0., 8., defaults["stable_after_fall"] / C['days_per_year'], .25, key='stable'
) * C['days_per_year']

growth_stable = st.sidebar.slider(
    "How fast?", -.2, 1.2, defaults["growth_stable"], .1, key='stable'
)

st.sidebar.markdown("### 3️⃣ Recross BaseFunc from Below")

take_off_after_stable = st.sidebar.slider(
    "When?", 0., 8., defaults["take_off_after_stable"] / C['days_per_year'], .25, key='take_off'
) * C['days_per_year']

growth_take_off = st.sidebar.slider(
    "How fast?", -.2, 8., defaults["growth_take_off"], .1, key='take_off'
)

st.sidebar.markdown("### 4️⃣ Stabilize Above BaseFunc")

steady_after_take_off = st.sidebar.slider(
    "When?", 0., 8., defaults["steady_after_take_off"] / C['days_per_year'], .25, key='steady'
) * C['days_per_year']

growth_steady = st.sidebar.slider(
    "How fast?", -.2, 1.2, defaults["growth_steady"], .1, key='steady'
)

st.sidebar.markdown("## Compare Against")

SCENARIO2CHECKBOX = OrderedDict({
    "pessimistic-simple-mint": st.sidebar.checkbox("Simple Minting Only Scenario"),
    "optimistic": st.sidebar.checkbox("Optimistic Scenario"),
    "baseline": st.sidebar.checkbox("BaseFunc Scenario"),
})

st.sidebar.markdown("## Speed")

simulation_speed = st.sidebar.selectbox("Simulation Speed", ("Medium", "Fast", "Slow")).lower()


df = run_cadcad_model(
    fall_after_beginning=fall_after_beginning,
    growth_fall=growth_fall,
    stable_after_fall=stable_after_fall,
    growth_stable=growth_stable,
    take_off_after_stable=take_off_after_stable,
    growth_take_off=growth_take_off,
    steady_after_take_off=steady_after_take_off,
    growth_steady=growth_steady,
)

comparison_df = df[df['scenario'].isin([scenario for scenario, checked in SCENARIO2CHECKBOX.items() if checked])]
df = df[df['scenario'] == 'user']
num_steps = len(df)

# Simulate user scenario

prevrow = None

for i in range(num_steps if run_simulation else 1):
    row = df.iloc[[i]]
    # Update stats
    cols = stats_dboard.columns(len(stat2meta))
    for ((stat, meta), col) in zip(stat2meta.items(), cols):
        delta_func = meta.get("delta_func")
        value_func = meta.get("value_func", lambda x: x)
        format_func = meta.get("format_func", lambda x: x)
        if prevrow is not None and delta_func is not None:
            delta = delta_func(row[stat].item(), prevrow[stat].item())
            delta = meta.get("format_func", lambda x: x)(delta)
        else:
            delta = None
        value = format_func(value_func(row[stat].item()))
        with col:
            st.metric(label=meta["label"], value=value, delta=delta)
    # Update plots
    if i == 0:
        with plot_container:
            network_power_chart = NetworkPowerAltairChart.build(pd.concat([comparison_df, row]), num_steps)
            mining_utility_chart = MiningUtilityAltairChart.build(pd.concat([comparison_df, row]), num_steps)
    else:
        network_power_chart.add_rows(row)
        mining_utility_chart.add_rows(row)
    # Finally
    if run_simulation:
        frac_complete = (i + 1) / num_steps
        time.sleep(C['speed_to_latency'][simulation_speed])
        progress_bar.progress(frac_complete)
        progress_text.text(f"{(frac_complete * 100):.2f}% Complete")
        prevrow = row

# Download data

@st.cache
def convert_df(df):
    return df.to_csv().encode("utf-8")


with download_container:
    csv = convert_df(pd.concat([df, comparison_df]))
    st.text("Download raw simulation results as .csv.")
    st.download_button(
        label="Download",
        data=csv,
        file_name="filecoin_basefunc_sim_results.csv",
        mime="text/csv",
    )
