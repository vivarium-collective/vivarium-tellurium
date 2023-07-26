'''
Execute by running: ``python template/processes/template_process.py``
'''

from vivarium.core.process import Process
from vivarium.core.engine import Engine, pp
import tellurium as te


class TelluriumProcess(Process):
    '''
    Class which serves to be a Tellurium implementation of the `vivarium.core.processes.Process()` interface.
    '''
    
    defaults = {
        'sbml_model_path': '',
        'antimony_string': None,
        'exposed_species': None,  # list of exposed species ids
        'parameter1': 3.0,
    }

    def __init__(self, config=None):
        '''
        A new instance of a `tellurium`-based implementation of the `vivarium.core.processes.Process() interface.
        
        Instantiates a `roadrunner` simulator instance using either `SBML`(default,`file`) or `antimony`(optional,`str`)
        
        #### Parameters:
        ----------------
        parameters: `Dict`
            configurations of the simulator process parameters. Defaults to `defaults`:\n
                            `'sbml_model_file': ''`
                            `'antimony_string': None`
                            `'exposed_species': None`  # list of exposed species ids
                            `'parameter1': 3.0`
                            
        #### Returns:
        -------------
        `TelluriumProcess`
            A generic instance of a Tellurium simulator process.
        '''
        
        super().__init__(config)
        
        # initialize a tellurium(roadrunner) simulation object. Load the model in using either sbml(default) or antimony
        if self.parameters.get('antimony_string'):
            self.simulator = te.loada(self.parameters['antimony_string'])
        else:
            self.simulator = te.loadSBMLModel(self.parameters['sbml_model_file'])

        # extract the variables 
        self.species = self.simulator.get_species() # PLACEHOLDER!!!!!!!!
        

    def ports_schema(self):
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
    '''
    Run a test simulation process. Loaded using SBML.

    Returns:
        The simulation output.
    '''
    sbml_model_path = 'vivarium_tellurium/library/Caravagna-J-Theor-Biol-2010-tumor-suppressive-oscillations/Caravagna2010.xml'
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
        'sbml_model_path': sbml_model_path,
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
        'antimony_string': 'S1 -> S2; k1*S1'
    }

    # 3.) Initialize the process by passing in a config dict
    antimony_process = TelluriumProcess(config)
    print(antimony_process.simulator)


# run module with python template/processes/template_process.py
if __name__ == '__main__':
    test_tellurium_process()
    
