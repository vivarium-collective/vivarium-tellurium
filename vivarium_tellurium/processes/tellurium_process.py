"""
Execute by running: ``python vivarium_tellurium/processes/tellurium_process.py`
"""

from vivarium.core.process import Process
from vivarium.core.engine import Engine, pf
import tellurium as te


class TelluriumProcess(Process):
    """Vivarium Process interface for Tellurium"""
    
    defaults = {
        'sbml_model_path': '',
        'antimony_string': None,
    }

    def __init__(self, config=None):
        super().__init__(config)
        
        # initialize a tellurium(roadrunner) simulation object. Load the model in using either sbml(default) or antimony
        if self.parameters.get('antimony_string'):
            self.simulator = te.loada(self.parameters['antimony_string'])
        else:
            self.simulator = te.loadSBMLModel(self.parameters['sbml_model_path'])

        # TODO -- make this configurable.
        self.input_ports = [
            'floating_species',
            'boundary_species',
            # 'time',
            # 'compartments',
            # 'parameters',
            # 'stoichiometries',
        ]

        self.output_ports = [
            'floating_species',
            # 'time',
        ]

        # extract the variables
        # TODO -- get these according to ports
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
            'time': {
                '_default': 0.0,
                '_updater': 'set',
                '_emit': True,
            },
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
                '_default': self.reaction_list
            },
        }

    def next_update(self, interval, states):

        # set tellurium values according to what is passed in states
        for port_id, values in states.items():
            if port_id in self.input_ports:  # only update from input ports
                for cat_id, value in values.items():
                    self.simulator.setValue(cat_id, value)

        # run the simulation
        new_time = self.simulator.oneStep(states['time'], interval)

        # extract the results and convert to update
        update = {'time': new_time}
        for port_id, values in states.items():
            if port_id in self.output_ports:
                update[port_id] = {}
                for cat_id in values.keys():
                    update[port_id][cat_id] = self.simulator.getValue(cat_id)
        return update


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
    print(f'RESULTS: {pf(data)}')


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
    
