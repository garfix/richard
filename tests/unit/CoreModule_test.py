import unittest

from richard.core.Model import Model
from richard.core.Solver import Solver
from richard.core.constants import E1, E2
from richard.entity.Variable import Variable
from richard.module.CoreModule import CoreModule
from richard.entity.ExecutionContext import ExecutionContext


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

        bindings = self.core_module.equals([3, Variable('E1')], None)
        self.assertEqual(bindings, [[3, 3]])

        bindings = self.core_module.equals([Variable('E1'), 3], None)
        self.assertEqual(bindings, [[3, 3]])


    def test_let(self):

        model = Model([])
        solver = Solver(model)

        bindings = solver.solve([('let', E1, 5)])
        self.assertEqual(bindings, [{'E1': 5}])


    def test_unification(self):

        model = Model([])
        solver = Solver(model)

        source = [('alive', 'john'), ('lost', 'john'), ('likes', 'john', 'jane'), ('goal', 'john', ('win', 'jane'))]

        bindings = solver.solve([('$unification', source, [('lost', E1)])])
        self.assertEqual(bindings, [{'E1': 'john'}])

        bindings = solver.solve([('$unification', source, [('location', E1)])])
        self.assertEqual(bindings, [])

        bindings = solver.solve([('$unification', source, [('likes', E1, 'jane')])])
        self.assertEqual(bindings, [{'E1': 'john'}])

        bindings = solver.solve([('$unification', source, [('likes', E1, E1)])])
        self.assertEqual(bindings, [])

        bindings = solver.solve([('$unification', source, [('lost', E1), ('likes', E1, E2)])])
        self.assertEqual(bindings, [{'E1': 'john', 'E2': 'jane'}])

        bindings = solver.solve([('$unification', source, [('goal', E1, ('win', E2))])])
        self.assertEqual(bindings, [{'E1': 'john', 'E2': 'jane'}])

        bindings = solver.solve([('$unification', source, [('goal', E1, ('win', E1))])])
        self.assertEqual(bindings, [])

        bindings = solver.solve([('let', E2, 'mary'), ('$unification', source, [('lost', E1)])])
        self.assertEqual(bindings, [{'E1': 'john', 'E2': 'mary'}])

        bindings = solver.solve([('let', E1, 'mary'), ('$unification', source, [('lost', E1)])])
        self.assertEqual(bindings, [])

        # target, source
        bindings = solver.solve([('$unification', [('likes', E1, 'jane')], source)])
        self.assertEqual(bindings, [{'E1': 'john'}])

        bindings = solver.solve([('$unification', [('lost', E1)], source)])
        self.assertEqual(bindings, [{'E1': 'john'}])
