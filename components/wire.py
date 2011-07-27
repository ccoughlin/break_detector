#!/usr/bin/env python

'''wire.py - semi-realistic model of copper wire'''

import math
from components import resistor

class Wire(object):
    '''Model of Copper Wire'''
    resistivity = 6.69e-7

    def __init__(self, length, wire_gauge):
        self.gauge = wire_gauge
        self.length = length
        self.diameter = 0.
        self.nominal_resistance = 0.
        self.resistance = 0.
        self.maxcurrent = 0.
        self.calc_diameter()
        self.xsection = math.pi * math.pow(self.diameter/2, 2)
        self.broken = False

    @property
    def broken(self):
        '''Returns True if the wire is broken'''
        return self._broken
    @broken.setter
    def broken(self, is_broken=True):
        '''Breaks the wire - resistance goes to infinity, max current to 0'''
        self._broken = is_broken
        self.calc_resistance()
        self.calc_maxcurrent()
        
    def get_ratio(self, gauge):
        '''Returns the conversion factor between successive gauges.  Returns the gauge itself
        if 0-36; returns (1-# of zeroes) if '00' ('2/0'), '000' ('3/0'), '0000' ('4/0') are given.
        '''
        try:        
            if '/' in gauge:
                n = 1 - int(gauge.split('/')[0])
            elif int(gauge) == 0:
                n = 1 - int(gauge.count('0'))
            return n
        except (TypeError, ValueError):
            return int(gauge)

    def calc_diameter(self):
        '''Calculates the wire's diameter in inches based on its gauge'''
        self.diameter = 0.005 * math.pow(92., (36. - self.get_ratio(self.gauge))/39.)

    def calc_resistance(self):
        '''Calculates the nominal and actual resistance of the wire'''
        if not self.broken:
            self.nominal_resistance = Wire.resistivity * self.length / self.xsection
            self.resistance = resistor.Resistor(nominal_resistance = self.nominal_resistance, 
                tolerance = 0.01).resistance
        else:
            self.nominal_resistance = float('inf')
            self.resistance = float('inf')

    def calc_maxcurrent(self):
        '''Calculates the wire's current-carrying capability based on the 700 cmils / A rule of thumb'''
        if not self.broken:
            xsection_cmils = 4e6 * self.xsection / math.pi
            self.maxcurrent = xsection_cmils / 700.
        else:
            self.maxcurrent = 0.