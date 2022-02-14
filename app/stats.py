from collections import OrderedDict

from millify import millify
import numpy as np


def format_float_stat(stat):
    return f"{np.round(stat * 100, 2).item()}%"


def format_int_stat(stat):
    return millify(stat)


# TODO: add units


stat2meta = OrderedDict(
    {
        "years_passed": {"label": "Year"},
        "consensus_power_in_zib": {
            "label": "Quality-Adjusted Network Power",
            "delta_func": lambda curr, prev: curr - prev,
            "format_func": format_float_stat,
        },
        "block_reward_in_kfil": {
            "label": "Block Reward",
            "delta_func": lambda curr, prev: curr - prev,
            "format_func": format_float_stat,
        },
        "marginal_reward_per_power_in_fil_per_pib": {
            "label": "Marginal Reward",
            "delta_func": lambda curr, prev: curr - prev,
            "format_func": format_float_stat,
        },
        "utility": {
            "label": "Mining Utility",
            "delta_func": lambda curr, prev: curr - prev,
            "format_func": format_float_stat,
        }
    }
)
