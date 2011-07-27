#!/usr/bin/env python


'''test_resistor.py - tests the Resistor class'''

import unittest
from components import resistor

class TestResistor(unittest.TestCase):
    '''Unit tests for Resistor'''
    def setUp(self):
        self.nominal_resistance = 100.
        self.resistor_tolerance = 0.05
        self.resistor = resistor.Resistor(nominal_resistance = self.nominal_resistance,
            tolerance = self.resistor_tolerance)

    def test_resistance(self):
        '''Verify that the resistance is within the specified tolerance of the nominal resistance'''
        lower_limit = self.nominal_resistance * (1 - self.resistor_tolerance)
        upper_limit = self.nominal_resistance * (1 + self.resistor_tolerance)
        self.assertTrue(self.resistor.resistance >= lower_limit and self.resistor.resistance <= upper_limit)

    def test_series_resistance(self):
        '''Verify simplifying series of resistors'''
        resistorA = resistor.Resistor(nominal_resistance = 100.)
        resistorB = resistor.Resistor(nominal_resistance = 200.)
        resistorC = resistor.Resistor(nominal_resistance = 300.)
        series_sum = resistorA.resistance + resistorB.resistance + resistorC.resistance
        self.assertAlmostEqual(series_sum, resistor.SeriesResistance([resistorA, resistorB, resistorC]))

    def test_parallel_resistance(self):
        '''Verify simplifying parallel networks of resistors'''
        resistorA = resistor.Resistor(nominal_resistance = 100.)
        resistorB = resistor.Resistor(nominal_resistance = 200.)
        resistorC = resistor.Resistor(nominal_resistance = 300.)
        parallel_sum = 1/(1/resistorA.resistance + 1/resistorB.resistance + 1/resistorC.resistance)
        self.assertAlmostEqual(parallel_sum, resistor.ParallelResistance([resistorA, resistorB, resistorC]))

    def test_zero_resistance(self):
        '''Verify handling zero resistance in parallel'''
        resistorA = 0
        resistorB = 10
        resistorC = 0
        resistance = resistor.ParallelResistance([resistorA, resistorB, resistorC])
        self.assertAlmostEqual(resistance, 0)

    def test_inf_resistance(self):
        '''Verify handling infinite resistance in parallel'''
        resistorA = 23
        resistorB = 111
        resistorC = float('inf')
        resistance = resistor.ParallelResistance([resistorA, resistorB, resistorC])
        ABresistance = resistor.ParallelResistance([resistorA, resistorB])
        self.assertAlmostEqual(resistance, ABresistance)