from vivarium_tellurium.processes.tellurium_process import TelluriumProcess 


class AntimonyTelluriumProcess(TelluriumProcess):
    
    defaults = {
        'api': 'tellurium',
        'api_imports': [
            'loada'
        ],
        'antimony_string': None,
    }
    
    def __init__(self, parameters=None):
        '''
        An instance of `TelluriumProcess` that is dedicated to executing simulations with Antimony strings.
        '''
        
        super().__init__(parameters)
        
        
    """TODO: Add ports_schema() and next_update() and handlers"""
    
    
def test_antimony_tellurium_process():
    return None 


if __name__ == '__main__':
    test_antimony_tellurium_process()
        