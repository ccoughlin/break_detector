#!/usr/bin/env python

''' analysis.py - analyzes results of a break_detector run '''

import os.path

class Analysis(object):
    '''Reads and analyzes the results of a break_detector run'''
    def __init__(self, simresults, threshold=0.1):
        self.results_fn = simresults
        self.threshold = threshold
        self.resistances = {}

    def check_obvious_collisions(self):
        '''Checks for obvious collisions in the simulation results:
        a single resistance reading caused by more than one combination
        of sensor failures
        '''
        if os.path.exists(self.results_fn):
            collisions = {}
            with open(self.results_fn,'rb') as results:
                for line in results:
                    if not line.startswith('#'):
                        elements = line.strip().split(',')
                        resistance_reading = elements[1]
                        failures = sorted(elements[2:])
                        # Checks for collisions in the data -
                        # a single resistance reading caused by
                        # more than one combination of failed
                        # sensors
                        if not resistance_reading in self.resistances:
                            self.resistances[resistance_reading] = failures
                        else:
                            if self.resistances[resistance_reading] != failures:
                                collisions[resistance_reading] = (self.resistances[resistance_reading], failures)
            return collisions
        else:
            raise IOError("File not found")