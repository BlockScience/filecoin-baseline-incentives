import os
import streamlit as st

from chart import *
from description import description
from glossary import glossary
from model import run_cadcad_model
from utils import load_constants


C = CONSTANTS = load_constants()

# Define layout

st.set_page_config(
    page_title="Filecoin Consensus Pledge Educational Calculator",
    page_icon=os.path.join(os.path.dirname(__file__), "assets", "icon.png"),
    layout="wide",
)

st.markdown("# Filecoin Consensus Pledge Educational Calculator")

st.markdown(
    """
This app allows you to **interactively understand Baseline Minting** through the lens of both mining incentives and **crossing the Baseline Function up or down**.

You have full control over the raw-bytes Network Power trajectory! That's the `user`, and by tweaking the `How long? (in years since last change)` and `rb-NP growth (as a fraction of the baseline growth)` fields for each stage, you can **observe its behavior, and compare to it to that of other baseline scenarios.**
"""
)

with st.expander("See description"):
    description()

st.markdown("# Graphs")
plot_container = st.container()

st.markdown("# Glossary")
glossary_container = st.container()
with glossary_container:
    with st.expander("See glossary"):
        glossary()

st.markdown("# Download")
download_container = st.container()

# Define sidebar


_, image_container, _ = st.sidebar.columns([1, 2, 1])

with image_container:
    st.image(os.path.join(os.path.dirname(__file__), "assets", "icon.png"))

st.sidebar.markdown("# Parameters for the `user` scenario")

defaults = C

st.sidebar.markdown(
    """
The trajectory is described as being:
1. First, the rb-NP is set to a fixed initial value.
2. For a given duration, the rb-NP grows as a fraction of the Baseline Function growth. Those are the parameters for the (Cross BaseFunc from Above) stage.
3. Repeat `2.` for the remaining phases.
"""
)

st.sidebar.markdown(
"""## Phase one"""
)
duration_1 = st.sidebar.slider(
    "Duration in Days", 0, 560, defaults["duration_1"], 7, key="duration_1"
)

new_sector_rb_onboarding_rate_1 = st.sidebar.slider(
    "RB Onboarding Rate (PiB)", 0.0, 100.0, defaults["new_sector_rb_onboarding_rate_1"], 0.1, key="new_sector_rb_onboarding_rate_1"
)

new_sector_quality_factor_1 = st.sidebar.slider(
    "RB Onboarding QF", 1.0, 10.0, defaults["new_sector_quality_factor_1"], 0.1, key="new_sector_quality_factor_1"
)

new_sector_lifetime_1 = st.sidebar.slider(
    "New Sector Lifetime", 180, 360, defaults["new_sector_lifetime_1"], 1, key="new_sector_lifetime_1"
)

renewal_probability_1 = st.sidebar.slider(
    "Daily Renewal Probability (%)", 0.0, 10.0, defaults["renewal_probability_1"], 0.1, key="renewal_probability_1"
)

st.sidebar.markdown(
"""## Phase two"""
)

new_sector_rb_onboarding_rate_2 = st.sidebar.slider(
    "RB Onboarding Rate (PiB)", 0.0, 100.0, defaults["new_sector_rb_onboarding_rate_2"], 0.1, key="new_sector_rb_onboarding_rate_2"
)

new_sector_quality_factor_2 = st.sidebar.slider(
    "RB Onboarding QF", 1.0, 10.0, defaults["new_sector_quality_factor_2"], 0.1, key="new_sector_quality_factor_2"
)

new_sector_lifetime_2 = st.sidebar.slider(
    "New Sector Lifetime", 180, 360, defaults["new_sector_lifetime_2"], 1, key="new_sector_lifetime_2"
)

renewal_probability_2 = st.sidebar.slider(
    "Daily Renewal Probability (%)", 0.0, 10.0, defaults["renewal_probability_2"], 0.1, key="renewal_probability_2"
)

# st.sidebar.markdown("## Compare Against")

# SCENARIO2CHECKBOX = OrderedDict(
#     {
#         "user-baseline-deactivated": st.sidebar.checkbox("User + BaseFunc Deactivated Scenario", value=True),
#         "optimistic": st.sidebar.checkbox("Optimistic Scenario", value=True),
#         "baseline": st.sidebar.checkbox("BaseFunc Scenario", value=True),
#     }
# )

# Run model

df = run_cadcad_model(duration_1, new_sector_rb_onboarding_rate_1, new_sector_quality_factor_1, new_sector_lifetime_1, renewal_probability_1 / 100,
                      new_sector_rb_onboarding_rate_2, new_sector_quality_factor_2, new_sector_lifetime_2,
                       renewal_probability_2 / 100)
# df = df[df["scenario"].isin(["user"] + [scenario for scenario, checked in SCENARIO2CHECKBOX.items() if checked])]

# Plot results


user_df = df.query("scenario == 'user'")
with plot_container:
    num_steps = df.timestep.nunique()
    vline = duration_1 / 365.25
    network_power_chart = NetworkPowerPlotlyChart.build(user_df, num_steps, vline)
    qa_power_chart = QAPowerPlotlyChart.build(user_df, num_steps)
    onboarding_collateral_chart = OnboardingCollateralPlotlyChart.build(user_df, num_steps, vline)
    circulating_supply_chart = CirculatingSupplyPlotlyChart.build(df, num_steps, vline)
    token_dist_chart = TokenDistributionPlotlyChart.build(df, num_steps, vline)
    locked_token_dist_chart = TokenLockedDistributionPlotlyChart.build(df, num_steps, vline)
    critical_cost_chart = CriticalCostPlotlyChart.build(df, num_steps, vline)
    circulating_surplus_chart = CirculatingSurplusPlotlyChart.build(df, num_steps, vline)
    effective_network_time_chart = EffectiveNetworkTimePlotlyChart.build(user_df, num_steps)
    simple_reward_chart = SimpleRewardPlotlyChart.build(user_df, num_steps)
    baseline_reward_chart = BaselineRewardPlotlyChart.build(user_df, num_steps)
    marginal_reward_chart = MarginalRewardPlotlyChart.build(user_df, num_steps)
    

# Download data


@st.cache
def convert_df(df):
    return df.to_csv().encode("utf-8")


with download_container:
    csv = convert_df(df)
    st.text("Download raw simulation results as .csv.")
    st.download_button(
        label="Download",
        data=csv,
        file_name="filecoin_basefunc_sim_results.csv",
        mime="text/csv",
    )
