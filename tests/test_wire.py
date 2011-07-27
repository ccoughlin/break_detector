#!/usr/bin/env python


'''test_wire.py - tests the Wire class'''

import unittest
import math
from components import wire

class TestWire(unittest.TestCase):
    '''Unit tests for Wire'''
    def setUp(self):
        self.wire_diameter_36awg = 0.0050
        self.wire_diameter_10awg = 0.1019
        self.wire_diameter_0000awg = 0.4600
        self.wire_diameter_00awg  = 0.3648
        self.wire_36awg = wire.Wire(length=100, wire_gauge=36)
        self.wire_10awg = wire.Wire(length=100, wire_gauge=10)
        self.wire_0000awg = wire.Wire(length=100, wire_gauge="0000")
        self.wire_00awg = wire.Wire(length=100, wire_gauge="2/0")

    def test_wire_dia(self):
        '''Verify specifying wire gauge creates correct diameter'''
        self.assertAlmostEqual(self.wire_36awg.diameter, self.wire_diameter_36awg,
            delta=self.wire_diameter_36awg/100.)
        self.assertAlmostEqual(self.wire_10awg.diameter, self.wire_diameter_10awg,
            delta=self.wire_diameter_10awg/100.)
        self.assertAlmostEqual(self.wire_0000awg.diameter, self.wire_diameter_0000awg,
            delta=self.wire_diameter_0000awg/100.)
        self.assertAlmostEqual(self.wire_00awg.diameter, self.wire_diameter_00awg,
            delta=self.wire_diameter_00awg/100.)

    def test_wire_xsection(self):
        '''Verify cross-sectional area calcs'''
        def xsection(radius):
            '''Calculates the cross-sectional area of a circle with the given radius'''
            return math.pi * math.pow(radius, 2)
        self.assertAlmostEqual(self.wire_36awg.xsection, xsection(self.wire_diameter_36awg/2),
            delta=self.wire_36awg.xsection/100.)
        self.assertAlmostEqual(self.wire_10awg.xsection, xsection(self.wire_diameter_10awg/2),
            delta=self.wire_10awg.xsection/100.)
        self.assertAlmostEqual(self.wire_0000awg.xsection, xsection(self.wire_diameter_0000awg/2),
            delta=self.wire_0000awg.xsection/100.)
        self.assertAlmostEqual(self.wire_00awg.xsection, xsection(self.wire_diameter_00awg/2),
            delta=self.wire_00awg.xsection/100.)
        
    def test_getgauge_ratio(self):
        '''Verify calculation of ratio in AWG => diameter'''
        wire_0awg_numeric = wire.Wire(length=1, wire_gauge=0)
        wire_0awg_string1 = wire.Wire(length=1, wire_gauge='0')
        wire_0awg_string2 = wire.Wire(length=1, wire_gauge='1/0')
        self.assertAlmostEqual(wire_0awg_numeric.diameter, wire_0awg_string1.diameter,
            delta=wire_0awg_numeric.diameter/100.)
        self.assertAlmostEqual(wire_0awg_numeric.diameter, wire_0awg_string1.diameter,
            delta=wire_0awg_numeric.diameter/100.)
        self.assertAlmostEqual(wire_0awg_numeric.diameter, wire_0awg_string2.diameter,
            delta=wire_0awg_numeric.diameter/100.)

    def test_maxcurrent(self):
        '''Verify calculation of max power transmission current'''
        self.assertAlmostEqual(self.wire_0000awg.maxcurrent, 302.,
            delta=30.2)
        self.assertAlmostEqual(self.wire_00awg.maxcurrent, 190.,
            delta=19.)
        self.assertAlmostEqual(self.wire_36awg.maxcurrent, 0.035,
            delta=0.0035)

    def test_wirebreak(self):
        '''Verify resistance goes to infinity and maxcurrent to 0 for a broken wire'''
        broken_lead = wire.Wire(length=144, wire_gauge=2)
        broken_lead.broken = True
        self.assertTrue(math.isinf(broken_lead.resistance))
        self.assertEqual(broken_lead.maxcurrent, 0.)