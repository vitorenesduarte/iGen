import sys
import unittest

if __name__ == '__main__':
    test_names = ['test_i_util']
    suite = unittest.defaultTestLoader.loadTestsFromNames(test_names)
    result = unittest.TextTestRunner().run(suite)
