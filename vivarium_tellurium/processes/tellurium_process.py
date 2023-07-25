'''
Execute by running: ``python template/processes/template_process.py``
'''

from importlib import import_module
from vivarium.core.process import Process
from vivarium.core.engine import Engine, pp

import tellurium as te


class TelluriumProcess(Process):
    '''
    Class which serves to be a Tellurium implementation of the `vivarium.core.processes.Process()` interface.
    '''
    
    defaults = {
        # 'api': 'tellurium',
        'api_imports': [],
        'model_file': '',
        'parameter1': 3.0,
        'antimony_string': None,
        'exposed_species': None,  # list of exposed species ids
    }

    def __init__(self, config=None):
        '''
        A new instance of a `tellurium`-based implementation of the `vivarium.core.processes.Process() interface.
        
        Imports content from simulator (model) module. Parameters passed into the constructor merge with the defaults\n
        and can be access through the self.parameters class variable.
        
        #### Parameters:
        ----------------
        parameters: `Dict`
            configurations of the simulator process parameters. Defaults to `defaults`:\n
                            `'api': 'tellurium',`
                            `'api_imports': [],`
                            `'model_file': '',`
                            `'parameter1': 3.0,`
                            
        #### Returns:
        -------------
        `TelluriumProcess`
            A generic instance of a Tellurium simulator process.
        '''
        super().__init__(config)

        if self.parameters.get('antimony_string'):
            pass

        # initialize a tellurium simulation object. Load the model in. Extract the variables.
        self.tellurium_object = te.load()

        self.species = self.tellurium_object.get_species()
        

    def ports_schema(self):
        '''
        ports_schema returns a dictionary that declares how each state will behave.
        Each key can be assigned settings for the schema_keys declared in Store:

        * `_default`
        * `_updater`
        * `_divider`
        * `_value`
        * `_properties`
        * `_emit`
        * `_serializer`
        '''

        # TODO -- need to set the ports/variables according to self.config assignments. Similar to viv-biosimul
        species_schema = {
            species_id: {
                    '_default': 1.0,
                    '_updater': 'set',
                    '_emit': True,
                } for species_id in self.config['exposed_species']
        }

        return {
            'species': species_schema
        }

    def next_update(self, interval, states):

        # set the states in tellurium according to what is passing in states
        for species_id, value in states['species'].items():
            self.tellurium_object.set_species(species_id, value)

        # run the simulation
        self.tellurium_object.simulate(0, interval, 1)

        # extract the results. TODO -- get the final values of the self.config['exposed_species'] and put them in the update
        update = {'species': {}}
        results = self.tellurium_object.get_data()

        return update


# functions to configure and run the process
def test_tellurium_process():
    '''Run a simulation of the process.

    Returns:
        The simulation output.
    '''
    
    # 1.) Declare the initial state, mirroring the ports structure. May be passed as a parsable argument.
    initial_state = {
        'internal': {
            'A': 0.0
        },
        'external': {
            'A': 1.0
        },
    }
    
    # 2.) Create the simulation run parameters for the simulator
    config = {
        'parameter1': 4.0,
    } 
            
    # 3.) Initialize the process by passing in a config dict
    template_process = TelluriumProcess(config)
    
    # 4.) Get the ports for the process
    template_process_ports = template_process.ports_schema()

    # 4a.) view the ports:
    print(f'PORTS FOR {pp(template_process)}: {pp(template_process_ports)}')
    
    #5.) Feed the Simulator Process instance you just created to the vivarium Engine
    sim = Engine(
        processes={
            'template': template_process,
        },
        topology={
            'template': {
                port_id: (port_id,) for port_id in template_process_ports.keys()
            },
        },
        initial_state=initial_state
    )
    
    #6.) Call update with that sim object, which calls the next_update method in the implementation you created above using total_time
    total_time = 3
    sim.update(
        interval=total_time
    )
    
    #7.) Get the data which is emitted from the sim object.
    data = sim.emitter.get_timeseries()
    
    #7a.) Observe the data which is return from running the process:
    print(f'RESULTS: {pp(data)}')
    return data


def test_load_from_antimony():
    config = {
        'antimony_string': ''
    }

    # 3.) Initialize the process by passing in a config dict
    template_process = TelluriumProcess.init_from_antimony(config)


# run module with python template/processes/template_process.py
if __name__ == '__main__':
    test_tellurium_process()
