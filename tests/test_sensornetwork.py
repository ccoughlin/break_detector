#!/usr/bin/env python


'''test_sensornetwork.py - tests the SensorNetwork class'''

import unittest
import os
import os.path
import tempfile
from components import sensornetwork
from components import resistor

class TestNetwork(unittest.TestCase):
    '''Unit tests for SensorNetwork'''
    def setUp(self):
        self.mean_time_to_failure = 15.
        self.shape = 3.
        self.resistances = [1e3, 2e3, 3e3, 4e3, 5e3]
        self.part_configs = []
        for resistance in self.resistances:
            part_config = {'mttf':self.mean_time_to_failure,
                'resistance':resistance}
            self.part_configs.append(part_config)
        self.sensor_net = sensornetwork.SensorNetwork(self.part_configs)

    def test_initial_time(self):
        '''Verify sensor network starts at time = 0 cycles '''
        self.assertEqual(self.sensor_net.cycle_num, 0)

    def test_initial_resistance(self):
        '''Verify initial resistance of the network'''
        self.assertAlmostEqual(self.sensor_net.resistance,
            resistor.ParallelResistance(self.resistances),
            delta=resistor.ParallelResistance(self.resistances)/10.)

    def test_initial_failures(self):
        '''Verify no parts of the network are broken at start time'''
        self.assertEqual(len(self.sensor_net.failures()), 0)

    def test_find_part_unspecified_name(self):
        '''Verify that an instrumented part can be found by an unspecified name'''
        part_one_config = {'mttf':self.mean_time_to_failure, 
            'resistance':self.resistances[0],
            'length':18., 
            'gauge':24}
        part_two_config = {'mttf':self.mean_time_to_failure, 
            'resistance':self.resistances[0],
            'length':18., 
            'gauge':24, 
            'name':'Kevlar Strand 33'}
        sensor_net = sensornetwork.SensorNetwork([part_one_config, part_two_config])
        part_one_name = str(part_one_config["resistance"])
        part_one_search = sensor_net.get_part(part_one_name)
        self.assertEqual(part_one_name, part_one_search[0].name)
        self.assertAlmostEqual(part_one_config["resistance"], part_one_search[0].resistance,
            delta=part_one_config["resistance"]/10.)

    def test_find_part_specified_name(self):
        '''Verify that an instrumented part can be found by a specified name'''
        part_one_config = {'mttf':self.mean_time_to_failure, 
            'resistance':self.resistances[0],
            'length':18., 
            'gauge':24}
        part_two_config = {'mttf':self.mean_time_to_failure, 
            'resistance':self.resistances[0],
            'length':18., 
            'gauge':24, 
            'name':'Kevlar Strand 33'}
        sensor_net = sensornetwork.SensorNetwork([part_one_config, part_two_config])
        part_two_search = sensor_net.get_part(part_two_config["name"])
        self.assertEqual(part_two_config["name"], part_two_search[0].name)
        self.assertAlmostEqual(part_two_config["resistance"], part_two_search[0].resistance,
            delta=part_two_config["resistance"]/10.)

    def test_find_nopart(self):
        '''Verify that a search for an instrumented part not in the
        network returns an empty list'''
        self.assertEqual([], self.sensor_net.get_part("Nylon Strand Delta"))

    def test_complete_failures(self):
        '''Verify at some distant point in the future that all the parts
        have failed'''
        part_configs = []
        for resistance in self.resistances:
            part_config = {'mttf':self.mean_time_to_failure,
                'resistance':resistance}
            part_configs.append(part_config)
        sensor_net = sensornetwork.SensorNetwork(part_configs)
        sensor_net.cycles = self.mean_time_to_failure * 1001
        self.assertEqual(len(sensor_net.failures()),
            len(self.resistances))

    def test_resistance_complete_failures(self):
        '''Verify at some distant point in the future the sensor network's
        resistance goes to infinity (open circuit)'''
        sensor_net = sensornetwork.SensorNetwork(self.part_configs)
        sensor_net.cycles = self.mean_time_to_failure * 3135
        self.assertEqual(sensor_net.resistance, float('inf'))

    def test_complete_sim(self):
        '''Verify that the sensor network reports complete at some point in the testing'''
        num_cycles = self.mean_time_to_failure * 3
        part_configs = []
        for resistance in self.resistances:
            part_config = {'mttf':self.mean_time_to_failure,
                'resistance':resistance}
            part_configs.append(part_config)
        sensor_net = sensornetwork.SensorNetwork(part_configs)
        for cycle in xrange(int(num_cycles)):
            sensor_net.cycles = cycle
        self.assertTrue(sensor_net.complete())

    def test_simulate_returns_dict(self):
        '''Verify a single run of a simulation returns a dict of resistance, failures'''
        sim_result = sensornetwork.simulate(num_cycles=3*self.mean_time_to_failure,
            part_configurations = self.part_configs)
        self.assertIsInstance(sim_result, dict)

    def test_simulate(self):
        '''Verify a single simulation run returns 0 or more failures per resistance reading'''
        sim_result = sensornetwork.simulate(num_cycles=3*self.mean_time_to_failure,
            part_configurations=self.part_configs)
        for key, failures_str in sim_result.items():
            # Ensure float() doesn't raise ValueError in converting key
            float(key)
            if failures_str != '':
                failures = failures_str.split(',')
                self.assertTrue(len(failures)>0)

    def test_singlecore_simulation_output(self):
        '''Verify the single-core run produces an output file'''
        output_file = os.path.join(tempfile.gettempdir(), 'single_core.csv')
        sensornetwork.run_simulation(num_simulations=2, num_cycles=self.mean_time_to_failure*3,
            part_configurations=self.part_configs, start_time=0, fname=output_file)
        self.assertTrue(os.path.getsize(output_file) > 0)
        os.remove(output_file)

    def test_multicore_simulation_output(self):
        '''Verify the multi-core run produces an output file'''
        output_file = os.path.join(tempfile.gettempdir(), 'multi_core.csv')
        sensornetwork.run_simulation(num_simulations=2, num_cycles=self.mean_time_to_failure*3,
            part_configurations=self.part_configs, start_time=0, fname=output_file)
        self.assertTrue(os.path.getsize(output_file) > 0)
        os.remove(output_file)
