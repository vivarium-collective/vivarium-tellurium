"""
Execute by running: ``python vivarium_tellurium/processes/tellurium_process.py`
"""

from vivarium.core.process import Process
from vivarium.core.engine import Engine, pp
import tellurium as te


class TelluriumProcess(Process):
    """Vivarium Process interface for Tellurium"""
    
    defaults = {
        'sbml_model_path': '',
        'antimony_string': None,
        # 'exposed_species': None,  # list of exposed species ids
    }

    def __init__(self, config=None):
        super().__init__(config)
        
        # initialize a tellurium(roadrunner) simulation object. Load the model in using either sbml(default) or antimony
        if self.parameters.get('antimony_string'):
            self.simulator = te.loada(self.parameters['antimony_string'])
        else:
            self.simulator = te.loadSBMLModel(self.parameters['sbml_model_path'])

        # extract the variables 
        self.floating_species_list = self.simulator.getFloatingSpeciesIds()
        self.boundary_species_list = self.simulator.getBoundarySpeciesIds()
        self.floating_species_initial = self.simulator.getFloatingSpeciesConcentrations()
        self.boundary_species_initial = self.simulator.getBoundarySpeciesConcentrations()
        self.reaction_list = self.simulator.getReactionIds()

    def initial_state(self, config=None):
        floating_species_dict = dict(zip(self.floating_species_list, self.floating_species_initial))
        boundary_species_dict = dict(zip(self.boundary_species_list, self.boundary_species_initial))
        return {
            'floating_species': floating_species_dict,
            'boundary_species': boundary_species_dict,
        }

    def ports_schema(self):
        return {
            'floating_species': {
                species_id: {
                    '_default': 1.0,
                    '_updater': 'set',
                    '_emit': True,
                } for species_id in self.floating_species_list
            },
            'boundary_species': {
                species_id: {
                    '_default': 1.0,
                    '_updater': 'set',
                    '_emit': True,
                } for species_id in self.boundary_species_list
            },
            'reactions': {
                '_default': self.reaction_list},
        }

    def next_update(self, interval, states):

        # set the states in tellurium according to what is passing in states
        for species_id, value in states['floating_species'].items():
            self.simulator.setValue(species_id, value)
        for species_id, value in states['boundary_species'].items():
            self.simulator.setValue(species_id, value)

        # run the simulation
        self.simulator.simulate(0, interval, 2)

        # extract the results
        final_concentrations = self.simulator.getFloatingSpeciesConcentrations()

        # convert to an update and return
        floating_species_dict = dict(zip(self.floating_species_list, final_concentrations))
        return {
            'floating_species': floating_species_dict
        }


# functions to configure and run the process
def test_tellurium_process():
    total_time = 5
    sbml_model_path = 'vivarium_tellurium/models/BIOMD0000000061_url.xml'  # Caravagna2010.xml'

    # Create the simulation run parameters for the simulator
    config = {
        'sbml_model_path': sbml_model_path,
    }
            
    # Initialize the process by passing in a config dict
    template_process = TelluriumProcess(config)

    # Get the ports for the process
    process_ports = template_process.ports_schema()

    # Get the initial state
    initial_state = template_process.initial_state()

    # Feed the Simulator Process you just created to the vivarium Engine
    sim = Engine(
        processes={
            'template': template_process,
        },
        topology={
            'template': {
                port_id: (port_id,) for port_id in process_ports.keys()
            },
        },
        initial_state=initial_state
    )
    
    # Call update with that sim object, which calls the next_update method in the implementation you created above using total_time
    sim.update(
        interval=total_time
    )
    
    # Get the data which is emitted from the sim object.
    data = sim.emitter.get_timeseries()
    
    # Observe the data which is return from running the process:
    print(f'RESULTS: {pp(data)}')


# def test_load_from_antimony():
#     # 1. Adding an antimony string to your config dict will allow for "antimony mode" to be turned on.
#     config = {
#         'antimony_string': 'S1 -> S2; k1*S1'
#     }
#
#     # 2. Initialize the process by passing in a config dict
#     antimony_process = TelluriumProcess(config)
#     print(antimony_process.simulator)


# run module with python vivarium_tellurium/processes/tellurium_process.py
if __name__ == '__main__':
    test_tellurium_process()
    # test_load_from_antimony()
    
