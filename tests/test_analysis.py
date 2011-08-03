#!/usr/bin/env python

'''test_analysis.py - tests the Analysis class'''

import unittest
import analysis
import os.path
import sys

class TestAnalysis(unittest.TestCase):
    '''Tests the Analysis class'''
    def setUp(self):
        self.sample_file = os.path.join(sys.path[0],
            "results.csv")
        self.threshold = 0.1
        self.analyzer = analysis.Analysis(self.sample_file, self.threshold)

    def test_badinitnofile(self):
        '''Verify exception if no filename provided'''
        with self.assertRaises(TypeError):
            analyzer = analysis.Analysis()

    def test_init(self):
        '''Verify creation of Analysis class'''
        analyzer = analysis.Analysis(self.sample_file, self.threshold)
        self.assertEqual(self.sample_file, analyzer.results_fn)
        self.assertEqual(self.threshold, analyzer.threshold)
        self.assertDictEqual({}, analyzer.resistances)

    def test_checknoresultsfile(self):
        '''Verify IOError raised if sim file not found'''
        sim = os.path.join(sys.path[0],
            "no_such_simulation_file.csv")
        analyzer = analysis.Analysis(sim)
        with self.assertRaises(IOError):
            collisions = analyzer.check_obvious_collisions()

    def test_check_obviousgoodresults(self):
        '''Verify that a known good simulation run (no collisions)
        checks out as ok with check_obvious_collisions()'''
        known_good_sim = os.path.join(sys.path[0],
            "known_good.csv")
        analyzer = analysis.Analysis(known_good_sim)
        collisions = analyzer.check_obvious_collisions()
        self.assertTrue(len(collisions)==0)

    def test_check_obviousbadresults(self):
        '''Verify that a known bad simulation run (collisions)
        checks out as not ok with check_obvious_collisions()'''
        known_bad_sim = os.path.join(sys.path[0],
            "known_collisions.csv")
        analyzer = analysis.Analysis(known_bad_sim)
        collisions = analyzer.check_obvious_collisions()
        self.assertTrue(len(collisions)>0)