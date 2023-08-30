"""
==================
Tellurium Composite
==================
"""
from vivarium.core.engine import Engine, pp
from vivarium.core.composer import Composer
from vivarium.library.pretty import format_dict
from vivarium_tellurium.processes.tellurium_process import TelluriumProcess


class TelluriumComposer(Composer):

    defaults = {
        'te1': {
            'sbml_model_path': 'vivarium_tellurium/models/BIOMD0000000061_url.xml',
        },
        'te2': {
            'sbml_model_path': 'vivarium_tellurium/models/BIOMD0000000061_url.xml',
        },
    }

    def __init__(self, config=None):
        super().__init__(config)

    def generate_processes(self, config):
        te1 = TelluriumProcess(self.config['te1'])
        te2 = TelluriumProcess(self.config['te1'])

        return {
            'te1': te1,
            'te2': te2,
        }

    def generate_topology(self, config=None):
        return {
            'te1': {
                'floating_species': ('floating_species_1',),
                'boundary_species': ('boundary_species_1',),
                'reactions': ('reactions_1',),
            },
            'te2': {
                'floating_species': ('floating_species_2',),
                'boundary_species': ('boundary_species_2',),
                'reactions': ('reactions_2',),
            },
        }


def test_tellurium_composite():
    total_time = 3

    # set config (this is also the default)
    config = {
        'te1': {
            'sbml_model_path': 'vivarium_tellurium/models/BIOMD0000000061_url.xml',
        },
        'te2': {
            'sbml_model_path': 'vivarium_tellurium/models/BIOMD0000000061_url.xml',
        },
    }

    # Initialize the composer by passing in a config dict
    te_composer = TelluriumComposer(config)

    # Generate a composite by calling the Composers' generate method
    te_composite = te_composer.generate()

    # Get the initial state
    initial_state = te_composite.initial_state()

    # Feed the composite instance you just created to the vivarium Engine
    sim = Engine(
        composite=te_composite,
        initial_state=initial_state
    )

    # Call update with that sim object, which calls the next_update method in the implementation you created above using total_time
    sim.update(total_time)

    # Get the data which is emitted from the sim object.
    data = sim.emitter.get_timeseries()

    # Observe the data which is return from running the process:
    print(f'RESULTS: {pp(data)}')


# run module with python vivarium_tellurium/processes/tellurium_composite.py
if __name__ == '__main__':
    test_tellurium_composite()
