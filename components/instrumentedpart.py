#!/usr/bin/env python

''' instrumentedpart.py - simulates a part that fails instrumented with
a resistor'''

from components import partfailure
from components import wire
from components import resistor

class BreakSensor(object):
    '''Creates the break sensor:  a standard resistor strapped to a part
    that breaks.'''
    def __init__(self, resistance, length, gauge):
        self.create_resistor(resistance)
        self.create_wire(length, gauge)

    def create_resistor(self, resistance):
        '''Creates the resistor used to detect the breakage of the part'''
        self.resistor = resistor.Resistor(resistance)

    def create_wire(self, length, gauge):
        '''Creates the wire leads used to connect the resistor'''
        self.wire = wire.Wire(length, gauge)

    @property
    def resistance(self):
        '''Returns the sensor's electrical resistance in ohms.'''
        return resistor.SeriesResistance([self.resistor, self.wire])

    @property
    def broken(self):
        '''Indicates that the instrumented part has failed and 
        so our sensor's leads are as well'''
        return self.wire.broken
    @broken.setter
    def broken(self, is_broken=True):
        '''Sets the sensor's condition to is_broken (True by default) -
        part has failed.'''
        self.wire.broken = is_broken

class Part(object):
    '''Model for an instrumented part'''
    def __init__(self, mttf, resistance, length=None, gauge=None, shape=None, 
        scale=None, name=None):
        self.create_part(mttf, shape, scale)
        self.create_breaksensor(resistance, length, gauge)
        if name is not None:
            self.name = name
        else:
            self.name = str(resistance)

    def create_part(self, mttf, shape, scale):
        '''Creates the part to fail being monitored'''
        if shape is None:
            shape = 3
        if scale is None:
            scale = 1
        self.part = partfailure.Part(mttf, shape, scale)

    def create_breaksensor(self, resistance, length, gauge):
        '''Creates the break sensor used to monitor the part'''
        if length is None:
            length = 6.
        if gauge is None:
            gauge = 24
        self.sensor = BreakSensor(resistance, length, gauge)

    @property
    def resistance(self):
        '''Returns the electrical resistance of the part'''
        return self.sensor.resistance

    @property
    def lifetime(self):
        '''Returns the lifetime in cycles of the part'''
        return self.part.lifetime

    def failed(self, cycle_number):
        '''Returns True if the part has failed by cycle_number'''
        part_failed = self.part.failed(cycle_number)
        if part_failed:
            self.sensor.broken = True
        return part_failed