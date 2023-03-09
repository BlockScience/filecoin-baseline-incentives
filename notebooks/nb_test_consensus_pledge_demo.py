# %%
import sys
sys.path.append('../')


# %%
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
# %%
from cadCAD_tools.preparation import sweep_cartesian_product
from consensus_pledge_model.params import INITIAL_STATE
from consensus_pledge_model.params import MULTI_RUN_PARAMS
from consensus_pledge_model.structure import CONSENSUS_PLEDGE_DEMO_BLOCKS
from cadCAD_tools import easy_run

N_timesteps = int(700 / 7)
N_samples = 1
# %%

sim_args = (INITIAL_STATE,
            sweep_cartesian_product(MULTI_RUN_PARAMS), 
            CONSENSUS_PLEDGE_DEMO_BLOCKS, 
            N_timesteps,
            N_samples)
sim_df = easy_run(*sim_args)

# %% [markdown]
"""
Exec times

N_t (#) | t (s)
- | -
10 | 0.17
20 | 0.63
30 | 1.44
40 | 2.5
80 | 10
90 | 14.7
180 | 98, 1.5min
210 | 95s
360 | 240, 4min (?)
"""

# %%
sim_df
# %%
sim_df.reward.map(lambda x: x.baseline_reward)
# %%
# x = sim_df.days_passed
# y = sim_df.baseline
# plt.plot(x, y, '.', markersize=1)

x = sim_df.days_passed
y = sim_df.power_rb
plt.plot(x, y, '.', markersize=1)

plt.show()
# %%
x = sim_df.days_passed
y = sim_df.power_qa
plt.plot(x, y, '.', markersize=1)
plt.show()
# %%
x = sim_df.days_passed
y = sim_df.token_distribution.map(lambda x: x.collateral)
plt.plot(x, y, '.', markersize=1)
plt.show()
# %%
x = sim_df.days_passed
y = sim_df.token_distribution.map(lambda x: x.locked_rewards)
plt.plot(x, y, '.', markersize=0.5)
plt.show()
# %%

x = sim_df.days_passed
y = sim_df.token_distribution.map(lambda x: x.circulating)
plt.plot(x, y, '.', markersize=0.5)
plt.show()

# %%

x = sim_df.days_passed
y = sim_df.token_distribution.map(lambda x: x.circulating / x.minted)
plt.plot(x, y, '.', markersize=0.5)
plt.show()

# %%

x = sim_df.days_passed
y = sim_df.token_distribution.map(lambda x: x.locked / x.available)
plt.plot(x, y, '.', markersize=0.5)
plt.show()

# %%

x = sim_df.days_passed
y = sim_df.token_distribution.map(lambda x: x.locked_rewards / x.available)
plt.plot(x, y, '.', markersize=0.5)
plt.show()

# %%

x = sim_df.days_passed
y = sim_df.token_distribution.map(lambda x: x.collateral / x.available)
plt.plot(x, y, '.', markersize=0.5)
plt.show()

# %%
x = sim_df.days_passed
y = sim_df.consensus_pledge_per_new_qa_power * sim_df.power_qa
plt.plot(x, y, '.', markersize=0.5)
plt.show()


# For 360 days of simulation:
# 360 new Aggregate Sectors
# For each sector: 180 Rewards to handle
# 360 Sectors * 180 Rewards = 64800 Rewards to Handle
# 360/2 Sectors * 180 Rewards * 360 days = 11.6M of reward data to store
# Incl substeps: 140M of reward data to store
# Assume unit of data = 8 bytes:
# 1119744000 bytes = 1.04 GB of data
# %%
x = sim_df.days_passed
y = sim_df.consensus_pledge_per_new_qa_power
plt.plot(x, y, '.', markersize=0.5)
plt.show()
# %%
x = sim_df.days_passed
y = sim_df.storage_pledge_per_new_qa_power
plt.plot(x, y, '.', markersize=0.5)
plt.show()
# %%
