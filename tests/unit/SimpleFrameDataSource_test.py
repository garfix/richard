import unittest

from richard.core.Model import Model
from richard.core.Solver import Solver
from richard.data_source.SimpleFrameDataSource import SimpleFrameDataSource
from richard.entity.Variable import Variable
from tests.unit.simple_frame_data_source.TestModule import TestModule


class TestSimpleFrameDataSource(unittest.TestCase):

    def test_simple_frame_datasource(self):

        model = Model([
            TestModule(SimpleFrameDataSource())
        ])

        solver = Solver(model)
        solver.write_atom(('goal', 1))

        self.assertEqual(solver.solve_single(('goal', Variable('E1')), {'B': 5}), [{'B': 5, 'E1': 1}])
        self.assertEqual(solver.solve_single(('goal', 1), {'B': 5}), [{'B': 5}])
        self.assertEqual(solver.solve_single(('goal', 2), {}), [])

        solver.write_atom(('goal', [('win', 'john', 'cup')]))
        solver.write_atom(('goal', [('win', 'mary', 'championship')]))

        self.assertEqual(solver.solve_single(('goal', [('win', Variable('E1'), Variable('E2'))]), {'X': 27}), [
            {'X': 27, 'E1': 'john', 'E2': 'cup'},
            {'X': 27, 'E1': 'mary', 'E2': 'championship'}])
        self.assertEqual(solver.solve_single(('goal', [('win', Variable('E1'), Variable('E1'))]), {}), [])
