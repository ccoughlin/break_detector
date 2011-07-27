#!/usr/bin/env python


'''test_instrumentedpart.py - tests the InstrumentedPart class'''

import unittest
from components import instrumentedpart
from components import resistor
from components import wire

class TestPart(unittest.TestCase):
    '''Unit tests for InstrumentedPart'''
    def setUp(self):
        self.sensor_length = 9.
        self.sensor_resistance = 1e3
        self.sensor_gauge = 24
        self.mean_time_to_failure = 15
        self.shape = 3

    def test_createsensor(self):
        '''Verify creation of break sensor'''
        sample_resistor = resistor.Resistor(nominal_resistance=self.sensor_resistance)
        sample_wire = wire.Wire(length=self.sensor_length, 
            wire_gauge=self.sensor_gauge)
        sensor = instrumentedpart.BreakSensor(self.sensor_resistance, 
            self.sensor_length, self.sensor_gauge)
        nominal_resistance = resistor.SeriesResistance([sample_resistor,
            sample_wire])
        self.assertAlmostEqual(sensor.resistance, nominal_resistance,
            delta=nominal_resistance/10.)
        self.assertAlmostEqual(sensor.resistance, nominal_resistance,
            delta=nominal_resistance/10.)

    def test_createpart(self):
        '''Verify creation of instrumented part'''
        sensor = instrumentedpart.BreakSensor(self.sensor_resistance,
            self.sensor_length, self.sensor_gauge)
        part = instrumentedpart.Part(mttf=self.mean_time_to_failure,
            resistance=self.sensor_resistance, length=self.sensor_length, 
            gauge=self.sensor_gauge)
        self.assertAlmostEqual(part.resistance, sensor.resistance,
            delta=sensor.resistance/10.)

    def test_partbreak(self):
        '''Verify the instrumented part's resistance goes to infinity
        when it breaks'''
        part = instrumentedpart.Part(mttf=self.mean_time_to_failure,
            resistance=self.sensor_resistance, length=self.sensor_length, 
            gauge=self.sensor_gauge)
        
        # Simulate a large number of cycles guaranteed to be equal to or
        # greater than the simulated lifetime of the part
        for cycle in xrange(self.mean_time_to_failure * 1000):
            if part.failed(cycle):
                nominal_resistance = float('inf')
                self.assertAlmostEqual(part.resistance, nominal_resistance,
                    delta=nominal_resistance/10)
                break
