import unittest

from richard.core.Model import Model
from richard.core.Solver import Solver
from richard.core.constants import E1
from richard.module.CoreModule import CoreModule
from richard.type.ExecutionContext import ExecutionContext


class TestCoreModule(unittest.TestCase):

    core_module: CoreModule

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.core_module = CoreModule()

    def test_equals(self):

        bindings = self.core_module.equals([3, 5], None)
        self.assertEqual(bindings, [])

        bindings = self.core_module.equals([3, 3], None)
        self.assertEqual(bindings, [[3, 3]])

        bindings = self.core_module.equals([3, None], None)
        self.assertEqual(bindings, [[3, 3]])

        bindings = self.core_module.equals([None, 3], None)
        self.assertEqual(bindings, [[3, 3]])


    def test_destructure(self):

        model = Model([])
        solver = Solver(model)

        source = [('alive', 'john'), ('lost', 'john')]

        bindings = solver.solve([('destructure', source, [('lost', E1)])])
        self.assertEqual(bindings, [{'E1': 'john'}])
