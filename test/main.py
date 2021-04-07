#  Copyright (c) 2021 Martin Staadecker under the MIT License

import unittest
from test.utilities import *

# Register all the functions in examples.stats
from examples.stats import *

# TODO complete

class FormulaTests(unittest.TestCase):
    def test_mean(self):
        mock_reader([3, 4])

        def callback(result):
            print("capture", result)
        run_and_capture(callback)