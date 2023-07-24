'''
Execute by running: ``python template/processes/template_process.py``

TODO: Replace the template code to implement your own process. 
'''

from vivarium.core.process import Process
from vivarium.core.engine import Engine, pp 


class Template(Process):
    '''
    This mock process provides a basic template that can be used for a new process
    '''

    # declare default parameters as class variables
    defaults = {
        'parameter1': 3.0,
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

    def next_update(self, timestep, states):

        # get the states
        internal_A = states['internal']['A']
        external_A = states['external']['A']

        # calculate timestep-dependent updates
        internal_update = self.parameters['parameter1'] * external_A * timestep
        external_update = -1 * internal_update

        # return an update that mirrors the ports structure
        return {
            'internal': {
                'A': internal_update},
            'external': {
                'A': external_update}
        }


# functions to configure and run the process
def test_template_process():
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
    template_process = Template(config)
    
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


# run module with python template/processes/template_process.py
if __name__ == '__main__':
    test_template_process()
