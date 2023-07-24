from vivarium_tellurium.processes.tellurium_process import TelluriumProcess 


class SBMLTelluriumProcess(TelluriumProcess):
    
    defaults = {
        'api': 'tellurium', 
        'api_imports': [
            '',
        ],
        'sbml_path': '',
    }
    
    def __init__(self, parameters=None):
        super().__init__(parameters)
        """TODO: Add ports_schema() and next_update() and handlers"""
        
def test_sbml_tellurium_process():
    return None 


if __name__ == '__main__':
    test_sbml_tellurium_process()