from vivarium.core.engine import Engine, pp 
from vivarium_tellurium.processes.tellurium_process import TelluriumProcess

"""
Test implementation file of a `TelluriumProcess` instance for Pytest.
"""


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