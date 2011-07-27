#!/usr/bin/env python

'''runtests.py - runs all the unit tests in the tests folder (Python 2.7 and above)'''

import unittest

if __name__ == "__main__":
    tests = unittest.TestLoader().discover(start_dir = "tests")
    unittest.TextTestRunner(verbosity=2).run(tests)