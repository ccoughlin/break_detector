#!/usr/bin/env python


'''test_partfailure.py - tests the Part class'''

import unittest
from components import partfailure

class TestPart(unittest.TestCase):
    '''Unit tests for Part'''
    def setUp(self):
        self.mean_time_to_failure = 15.
        self.shape = 3.
        self.parts = []
        for i in xrange(20):
            self.parts.append(partfailure.Part(mttf=self.mean_time_to_failure, shape=self.shape))

    def test_nofails_at_t0(self):
        '''Tests that a list of Parts correctly indicates no failures at time t = 0'''
        t0 = 0.
        for part in self.parts:
            self.assertFalse(part.failed(t0))   
        
    def test_allfails_at_tinf(self):
        '''Tests that all Parts have failed at an arbitrary number of cycles much greater than 
        their mean time to failure'''
        t100 = 117.3
        for part in self.parts:
            self.assertTrue(part.failed(t100))