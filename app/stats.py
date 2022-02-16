from collections import OrderedDict

from millify import millify
import numpy as np


def format_perc_float_stat(stat):
    return f"{np.round(stat * 100, 2).item()}%"


def format_float_stat(stat):
    return f"{np.round(stat, 2).item()}"


def format_bignum_int_stat(stat):
    if np.isnan(stat):
        return stat
    return millify(stat)


stat2meta = OrderedDict(
    {
        "years_passed": {
            "label": "Year",
            "format_func": format_float_stat
        },
        "network_power": {
            "label": "Network Power (QA PiB)",
            "delta_func": lambda curr, prev: curr - prev,
            "format_func": format_bignum_int_stat,
        },
        "block_reward": {
            "label": "Block Reward (FIL)",
            "delta_func": lambda curr, prev: curr - prev,
            "format_func": format_bignum_int_stat,
        },
        "marginal_reward": {
            "label": "Marginal Reward (FIL / QA PiB)",
            "delta_func": lambda curr, prev: curr - prev,
            "format_func": format_bignum_int_stat,
        },
        "mining_utility": {
            "label": "Mining Utility",
            "delta_func": lambda curr, prev: curr - prev,
            "format_func": format_float_stat,
        }
    }
)
