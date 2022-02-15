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
        'label': 'Evolve Network Power',
        'policies': {            
        }, 
        'variables': {
            'network_power': s_network_power
        }   
    },
    {
        'label': 'Update Capped Power',
        'policies': {            
        }, 
        'variables': {
            'cumm_capped_power': s_cumm_capped_power
        }   
    }
]