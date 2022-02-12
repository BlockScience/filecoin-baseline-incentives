from collections import OrderedDict

from millify import millify
import numpy as np


format_float_stat = lambda stat: f"{np.round(stat * 100, 2).item()}%"
format_int_stat = lambda stat: millify(stat)

stat2meta = OrderedDict(
    {
        "years_passed": {
            "label": "Year"
        },
        "consensus_power_in_zib": {
            "label": "Quality-Adjusted Network Power",
            "delta_func": lambda curr, prev: curr - prev,
            "format_func": format_float_stat,
        },
        "block_reward_in_kfil": {
            "label": "Block Reward",
            "delta_func": lambda curr, prev: curr - prev,
            "format_func": format_float_stat,
        }
    }
)
