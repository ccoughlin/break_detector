#!/usr/bin/env python

''' partfailure.py - simulates a component with a time to fail'''

import random

class Part(object):
    '''Simulates a part with a Weibull-distributed lifetime.'''
    def __init__(self, mttf, shape, scale=1.):
        random.seed()
        self.mttf = mttf
        self.lifetime = 0.
        self.gen_lifetime(shape, scale)

    def gen_lifetime(self, shape, scale):
        '''Generates a random lifetime for the part using Weibull random numbers.
        If 0 < shape < 1, the part exhibits infant mortality (more failures early in parts' life)
        If shape = 0, the part exhibits constant mortality
        If shape > 1, the part exhibits wear-out (more failures late in parts' life)
        '''
        self.lifetime = self.mttf * random.weibullvariate(alpha=scale, beta=shape)

    def failed(self, cycle_num):
        '''Returns True if the part has failed by this cycle, False if the part has not'''
        if cycle_num >= self.lifetime:
            return True
        else:
            return False