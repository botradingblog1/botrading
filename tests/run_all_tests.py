# tests/test_all.py
import unittest


# Discover all test cases in the tests directory
def suite():
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
