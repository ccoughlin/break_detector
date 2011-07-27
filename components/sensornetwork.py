#!/usr/bin/env python

'''sensornetwork.py - semi-realistic model of a network of instrumented parts'''

from components import instrumentedpart
from components import resistor
import operator
import itertools
import multiprocessing

class SensorNetwork(object):
    '''Simulates a network of instrumented parts'''

    def __init__(self, part_params, cycle_number = 0):
        self.parts = []
        self.create_parts(part_params)
        self.failed_parts = []
        self.status_log = {}
        self.cycle_num = cycle_number

    def create_parts(self, part_params):
        '''Creates the instrumented parts'''
        for part_config in part_params:
            if 'mttf' and 'resistance' in part_config:
                mttf = part_config.get('mttf')
                resistance = part_config.get('resistance')
                length = part_config.get('length', None)
                gauge = part_config.get('gauge', None)
                shape = part_config.get('shape', None)
                scale = part_config.get('scale', None)
                name = part_config.get('name', None)
                self.parts.append(instrumentedpart.Part(mttf, resistance, length, gauge, shape, scale, name))
        self.parts = sorted(self.parts, key=operator.attrgetter('lifetime'))

    def get_part(self, sensor_name):
        '''Returns a list of parts with the given name if found,
        empty list otherwise'''
        return [part for part in self.parts if part.name == sensor_name]

    @property
    def resistance(self):
        '''Returns the current network's electrical resistance in ohms.'''
        return resistor.ParallelResistance(
            [part.resistance for part in self.parts])

    @property
    def cycles(self):
        '''Returns the number of cycles experienced by the network.'''
        return self.cycle_num
    @cycles.setter
    def cycles(self, cyclenum):
        '''Sets the number of cycles in this network if at least one sensor is unbroken.'''
        if not self.complete():
            self.cycle_num = cyclenum
            self.failed_parts.extend(itertools.takewhile(
                lambda x: x.failed(self.cycle_num), self.parts))
            self.parts[:] = [part for part in self.parts 
                if not part.failed(self.cycle_num)]
            res_key = str(round(self.resistance, 1))
            if res_key not in self.status_log:
                self.status_log[res_key] = ','.join([part.name for part in self.failed_parts])

    def failures(self):
        '''Returns a list of the parts that have already failed'''
        return self.failed_parts

    def complete(self):
        '''Returns True if all the parts have failed and testing is complete'''
        return len(self.parts) == 0

def simulate(num_cycles, part_configurations, start_time=0):
    '''Runs a single simulation of the parts through num_cycles.  Returns a dict of the
    results - keys are the resistance in ohms of the network at a given condition,
    values are a comma-delimited string of the sensors that have failed at this resistance.'''
    sensor_sim = SensorNetwork(part_configurations, start_time)
    for cycle_num in xrange(int(start_time), int(num_cycles)):
        if not sensor_sim.complete():
            sensor_sim.cycles = cycle_num
        else:
            break
    return sensor_sim.status_log

def gen_header(num_simulations, num_cycles):
    '''Generates a simple file header for inclusion in the results output.'''
    header_str = ["# Monte Carlo Simulation Results\n",
        "# {0} simulations of {1} cycles\n".format(num_simulations, int(num_cycles)),
        "# Format:  Simulation Number, Resistance In Ohms, List of Failed Sensors\n"]
    return header_str

def run_simulation(num_simulations, num_cycles, part_configurations, start_time=0, fname="score.csv"):
    '''Runs num_simulations of a SensorNetwork of the provided
    parts starting at time cycle_number and running for num_cycles.
    Results are written to fname as ASCII delimited text.
    '''
    with open(fname, "wb") as fidout:
        fidout.writelines(gen_header(num_simulations, num_cycles))
        for simulation in xrange(num_simulations):
            simulation_run = simulate(num_cycles, part_configurations, start_time)
            for resistance_reading in simulation_run:
                output_str = "{0},{1},{2}\n".format(simulation,
                    resistance_reading, simulation_run.get(resistance_reading))
                fidout.write(output_str)

def multirun_simulation(num_simulations, num_cycles, part_configurations, start_time=0, num_processes=None,
    fname='mcore.csv'):
    '''Multi-process (defaults to cpu_count()) num_simulations runs of a SensorNetwork
    of the provided parts starting at time cycle_number and running for num_cycles.

    Results are written to fname as ASCII delimited text.
    '''
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    worker_pool = multiprocessing.Pool(num_processes)
    with open(fname, 'wb') as fidout:
        fidout.writelines(gen_header(num_simulations, num_cycles))
        for simulation in xrange(num_simulations):
            simulation_run = worker_pool.apply_async(simulate, [num_cycles, part_configurations, start_time]).get()
            for resistance_reading in simulation_run:
                output_str = "{0},{1},{2}\n".format(simulation,
                    resistance_reading, simulation_run.get(resistance_reading))
                fidout.write(output_str)
    worker_pool.close()
    worker_pool.join()

if __name__ == "__main__":
    # Demonstrates the use of the module, includes a simple timing to compare single vs. multiple core
    # usage.
    multiprocessing.freeze_support()
    import datetime
    
    simulations_to_run = 100000
    resistances = [1e3, 2e3, 3e3, 4e3, 5e3]
    mean_time_to_failure = 15.
    part_configs = []
    for partnum in resistances:
        part_config = {"mttf":mean_time_to_failure,
            "resistance":partnum}
        part_configs.append(part_config)
    
    print("Starting single-core run...")
    tstart = datetime.datetime.utcnow()
    run_simulation(simulations_to_run, mean_time_to_failure*3,
        part_configs)
    tfinish = datetime.datetime.utcnow()
    print("\n\n *** Single core time: {0} ***\n\n".format(tfinish-tstart))

    print("Starting multi-core run...")
    tstart2 = datetime.datetime.utcnow()
    multirun_simulation(simulations_to_run, mean_time_to_failure*3,
        part_configs)
    tfinish2 = datetime.datetime.utcnow()
    print("\n\n *** Multiple core time: {0} ***\n\n".format(tfinish2-tstart2))
