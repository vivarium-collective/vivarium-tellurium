import json 
from typing import Union
from importlib import import_module
import tellurium as te 
from vivarium.core.process import Process
from vivarium.core.engine import Engine, pp


class TelluriumProcess(Process):
    ''' Vivarium Process for Tellurium '''

    # declare default parameters as class variables
    defaults = {
        'api': 'tellurium',
        'api_imports': [],
        'model_path': '',
    }

    def __init__(self, parameters=None):
        '''
        A generic instance: Tellurium implementation of the `vivarium.core.processes.Process()` interface.
        
        Parameters passed into the constructor merge with the defaults and can be accessed through the `self.parameters` class attribute.
        
        #### Parameters:
        ----------------
            parameters:`Dict`
                default setting parameters for this Tellurium instance. Defaults to`None`.
        '''
        super().__init__(parameters)
        
        # import the necessary simulator api
        module = import_module(self.parameters['api'])
        # set the appropriate values from the given api content
        for content in self.parameters['api_imports']:
            self.__setattr__(content, getattr(module, content))

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


class AntimonyTelluriumProcess(TelluriumProcess):
    
    defaults = {
        'api': 'tellurium',
        'api_imports': ('loada'),
        'antimony_string': '',
    }
    
    def __init__(self, parameters=None):
        #instantiate the parent
        super().__init__(parameters)
        
        #get the tellurium package as an object
        tellurium = importlib.import_module(self.parameters['api'])
        
        #traverse the parameters to extract the package imports needed
        for content in self.parameters['api_imports']:
            self.__setattr__(content, getattr(tellurium, content))
            
            
    def next_update(self, interval, states, n_timesteps=100, antimony_string=None):
        # get the states from the tellurium model
        internal_A = states['internal']['A']
        external_A = states['external']['A']

        # run tellurium here
        antimony_string = antimony_string or self.parameters['antimony_string']
        internal_update = self.loada(antimony_string).simulate(0, interval, n_timesteps)
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
            


def test_process(process: Union[TelluriumProcess, AntimonyTelluriumProcess], 
                 process_name: str,
                 initial_state: dict, 
                 total_time: float,
                 config: dict = {}):
    proc = process(config)
    ports = proc.ports_schema()
    sim = Engine(
        processes={process_name: proc},
        topology={process_name: {port_id: (port_id,) for port_id in ports.keys()}},
        initial_state=initial_state
    )
    sim.update(total_time)
    return sim.emitter.get_data()
    

def test_tellurium():
    config = {}
    process = TelluriumProcess(config)
    name = 'tellurium'
    initial_state = {
        'internal': {
            'A': 0.0
        },
        'external': {
            'A': 1.0
        },
    }
    data = test_process(process, name, initial_state, 10.0, config)
    pp(data)
    
def test_antimony():
    config = {}
    process = AntimonyTelluriumProcess(config)
    process.parameters['antimony_string'] = 'S1 -> S2; k1*S1; k1 = 0.1; S1 = 10'
    config['antimony_string'] = 'S1 -> S2; k1*S1; k1 = 0.1; S1 = 10'
    name = 'antimony'
    initial_state = {
        'internal': {
            'A': 0.0
        },
        'external': {
            'A': 1.0
        },
    }
    ports = process.ports_schema()
    sim = Engine(
        processes={name: process},
        topology={name: {port_id: (port_id,) for port_id in ports.keys()}},
        initial_state=initial_state
    )
    sim.update(10.0)
    data = sim.emitter.get_data()
    pp(data)
    

def __test_tellurium():
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
    test_antimony()