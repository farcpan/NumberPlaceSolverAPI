import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lambda_functions import solver

import pytest


class Test_NumberPlaceSolver(object):
    @pytest.fixture
    def init_solver(self):
        print("Start.")
        self.s = solver.NumberPlaceSolver("000000000000000000000000000000000000000000000000000000000000000000000000000000000")
        print(self.s)

        yield
        print("End.")


    def test_solve(self, init_solver):
        result = self.s.solve(0)
        result_string = self.s.get_fields()

        assert result == True and len(result_string) == 81
