from consensus_pledge_model.logic import *

# TODO: Upgrade to the Consensus Pledge Model


BLOCKS = [
    {
        'label': 'Time Tracking',
        'policies': {
            'evolve_time': p_evolve_time
        },
        'variables': {
            'days_passed': s_days_passed,
            'delta_days': s_delta_days
        }
    },
    {
        'label': 'Evolve Network Power & Baseline Function',
        'policies': {            
        }, 
        'variables': {
            'network_power': s_network_power,
            'baseline': s_baseline
        }   
    },
    {
        'label': 'Update Capped Power',
        'policies': {            
        }, 
        'variables': {
            'cumm_capped_power': s_cumm_capped_power
        }   
    },
    {
        'label': '(Baseline) Effective Network Time',
        'policies': {    

        }, 
        'variables': {
            'effective_network_time': s_effective_network_time
        }   
    },
    {
        'label': 'Block Reward',
        'policies': {    

        }, 
        'variables': {
            'reward': s_reward
        }   
    }
]