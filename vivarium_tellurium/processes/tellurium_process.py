import json 
import tellurium as te 
from vivarium.core.process import Process
from vivarium.core.engine import Engine, pp


class TelluriumProcess(Process):
    ''' Vivarium Process for Tellurium '''

    # declare default parameters as class variables
    defaults = {
        'model_path': '',
        'uptake_rate': 0.1,
    }

    def __init__(self, parameters=None):
        # parameters passed into the constructor merge with the defaults
        # and can be access through the self.parameters class variable
        super().__init__(parameters)

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

        # TODO this needs to be done automatically by reading the tellurium model. Maybe study vivarium-biosimulators
        return {
            'internal': {
                'A': {
                    '_default': 1.0,
                    '_updater': 'accumulate',
                    '_emit': True,
                },
            },
            'external': {
                'A': {
                    '_default': 1.0,
                    '_updater': 'accumulate',
                    '_emit': True,
                },
            },
        }

    def next_update(self, interval, states):

        # get the states from the tellurium model
        internal_A = states['internal']['A']
        external_A = states['external']['A']

        # run tellurium here
        internal_update = self.parameters['uptake_rate'] * external_A * interval
        external_update = -1 * internal_update

        # get the results from tellurium
        update = {
            'internal': {
                'A': internal_update},
            'external': {
                'A': external_update}
        }

        # return an update that mirrors the ports structure
        return update




def test_tellurium():
    totaltime = 10.0

    # initialize the process
    config = {}
    tellurium_process = TelluriumProcess(config)

    # declare the initial state, mirroring the ports structure
    initial_state = {
        'internal': {
            'A': 0.0
        },
        'external': {
            'A': 1.0
        },
    }

    ports = tellurium_process.ports_schema()
    print('PORTS')
    print(ports)

    # make the simulation
    sim = Engine(
        processes={'tellurium_process': tellurium_process},
        topology={'tellurium_process': {port_id: (port_id,) for port_id in ports.keys()}},
        initial_state=initial_state
    )

    # run the simulation
    sim.update(totaltime)

    # get the results
    data = sim.emitter.get_data()

    print(pp(data))


if __name__ == '__main__':
    test_tellurium()