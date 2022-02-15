from baseline_model.logic import *

partial_state_update_blocks = [
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
        'policies': {
            'evolve_state': p_evolve_network
            
        }, 
        'variables': {
            'baseline_function': s_baseline_function,
            'network_power': s_network_power
        }   
    }
]