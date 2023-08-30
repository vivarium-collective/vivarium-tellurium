"""
==================
Tellurium Composite
==================
"""
from vivarium.core.engine import Engine, pf
from vivarium.core.composer import Composite
from vivarium_tellurium.processes.tellurium_process import TelluriumProcess


def test_tellurium_composite():
    total_time = 3

    # set config
    config = {
        'te1': {
            'sbml_model_path': 'vivarium_tellurium/models/BIOMD0000000061_url.xml',
        },
        'te2': {
            'sbml_model_path': 'vivarium_tellurium/models/BIOMD0000000061_url.xml',
        },
    }

    # make the processes
    processes = {
        'te1': TelluriumProcess(config['te1']),
        'te2': TelluriumProcess(config['te1']),
    }

    topology = {
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
    # Generate a composite by calling the Composers' generate method
    te_composite = Composite({
        'processes': processes,
        'topology': topology})

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
    print(f'Top-level stores: {list(data.keys())}')
    print(f'RESULTS: {pf(data)}')


# run module with python vivarium_tellurium/processes/tellurium_composite.py
if __name__ == '__main__':
    test_tellurium_composite()
