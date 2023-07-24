"""
==================
Template Composite
==================

This is a toy composite that loads in two template processes and combines them.
"""

# TODO: Delete this file before publishing your project.

from vivarium.core.engine import Engine, pp
from vivarium.core.composer import Composer
from vivarium.library.pretty import format_dict
from vivarium.processes.injector import Injector

from template.processes.template_process import Template


class TemplateComposer(Composer):

    defaults = {
        'template1': {
            'parameter1': 2.0,
        },
        'template2': {
            'parameter1': 5.0,
        },
    }

    def __init__(self, config=None):
        super().__init__(config)

    def generate_processes(self, config):
        template1 = Template(self.config['template1'])
        template2 = Template(self.config['template2'])

        return {
            'template1': template1,
            'template2': template2,
        }

    def generate_topology(self, config):
        return {
            'template1': {
                'internal': ('internal_1',),
                'external': ('external_shared', ),
            },
            'template2': {
                'internal': ('internal_2',),
                'external': ('external_shared', ),
            },
        }


def test_template_composite():
    '''Run a simulation of the composite.

    Returns:
        The simulation output.
    '''

    # 1.) Declare the initial state, mirroring the ports structure. May be passed as a parsable argument.
    initial_state = {
        'internal_1': {
            'A': 0.0
        },
        'internal_2': {
            'A': 10.0
        },
        'external_shared': {
            'A': 1.0
        },
    }

    # 2.) Create the simulation run parameters for the simulator
    config = {
        'template1': {
            'parameter1': 4.0,
        },
        'template2': {
            'parameter1': 4.0,
        }
    }

    # 3.) Initialize the composer by passing in a config dict
    template_composer = TemplateComposer(config)

    # 4.) Generate a composite by calling the Composers' generate method
    template_composite = template_composer.generate()

    # 5.) Feed the compsite instance you just created to the vivarium Engine
    sim = Engine(
        composite=template_composite,
        initial_state=initial_state
    )

    # 6.) Call update with that sim object, which calls the next_update method in the implementation you created above using total_time
    total_time = 3
    sim.update(
        interval=total_time
    )

    # 7.) Get the data which is emitted from the sim object.
    data = sim.emitter.get_timeseries()

    # 7a.) Observe the data which is return from running the process:
    print(f'RESULTS: {pp(data)}')
    return data


# run module with python template/processes/template_composite.py
if __name__ == '__main__':
    test_template_composite()
