#!/usr/bin/env python

'''resistor.py - semi-realistic model of a measured resistance'''

import random

class Resistor(object):
    '''Simple model of an electrical resistor, assumes uniform
    distribution of resistance around the nominal resistance value'''
    def __init__(self, nominal_resistance, tolerance = 0.05):
        random.seed()
        self.nominal_resistance = nominal_resistance
        self.tolerance = tolerance
        lower_limit = self.nominal_resistance * (1 - self.tolerance)
        upper_limit = self.nominal_resistance * (1 + self.tolerance)
        self.resistance = random.uniform(lower_limit, upper_limit)

def get_resistance(resistor):
    '''Returns resistor.resistance if an attribute of resistor,
    otherwise returns float(resistor).'''
    resistance = 0.
    if hasattr(resistor, 'resistance'):
        resistance = resistor.resistance
    else:
        resistance = float(resistor)
    return resistance

def SeriesResistance(resistors):
    '''Calculates the equivalent resistance of the resistors in series'''
    total_resistance = sum([get_resistance(resistor) for resistor in resistors])
    return total_resistance

def ParallelResistance(resistors):
    '''Calculates the equivalent resistance of the resistors in parallel'''
    resistances = [get_resistance(resistor) for resistor in resistors]
    if 0 in resistances:
        resistance = 0
    else:
        resistance_inverse = sum([1/resistance
        for resistance in resistances if resistance >0])
        if resistance_inverse != 0:
            resistance = 1/resistance_inverse
        elif resistance_inverse == 0:
            resistance = float('inf')
    return resistance
