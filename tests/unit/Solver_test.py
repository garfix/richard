import unittest

from richard.core.Model import Model
from richard.core.constants import E1, E2, IGNORED
from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.entity.Relation import Relation
from richard.interface import SomeSolver
from richard.interface.SomeDataSource import SomeDataSource
from richard.core.Solver import Solver
from richard.interface.SomeModule import SomeModule
from richard.store.MemoryDb import MemoryDb
from richard.store.Record import Record
from richard.type.ExecutionContext import ExecutionContext


class TestModule(SomeModule):
    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("river", query_function=self.simple_entity))
        self.add_relation(Relation("country", query_function=self.simple_entity))
        self.add_relation(Relation("contains", query_function=self.contains))
        self.add_relation(Relation("number_of", query_function=self.number_of))


    def simple_entity(self, values: list, context: ExecutionContext) -> list[list]:
        out_values = self.ds.select(context.relation.predicate, ['id'], values)
        return out_values


    def contains(self, values: list, context: ExecutionContext) -> list[list]:
        out_values = self.ds.select("contains", ['country', 'river'], values)
        return out_values


    def number_of(self, values: list, context: ExecutionContext) -> list[list]:
        out_values = [
            [None, 2]
        ]
        return out_values


class TestSolver(unittest.TestCase):

    def test_solver(self):

        db = MemoryDb()
        db.insert(Record('river', {'id': 'amazon'}))
        db.insert(Record('river', {'id': 'brahmaputra'}))

        db.insert(Record('country', {'id': 'brasil'}))
        db.insert(Record('country', {'id': 'india'}))

        db.insert(Record('contains', {'country': 'brasil', 'river': 'amazon'}))
        db.insert(Record('contains', {'country': 'india', 'river': 'brahmaputra'}))

        data_source = MemoryDbDataSource(db)
        model = Model([TestModule(data_source)])
        solver = Solver(model)


        tests = [
            [
                [('river', E1)],
                [{'E1': 'amazon'}, {'E1': 'brahmaputra'}]
            ],
            [
                [('river', E1), ('contains', 'india', E1)],
                [{'E1': 'brahmaputra'}]
            ],
            [
                [('contains', E1, E2), ('country', E1)],
                [{'E1': 'brasil', 'E2': 'amazon'},
                 {'E1': 'india', 'E2': 'brahmaputra'}]
            ],
            [
                [('contains', E1, E1)],
                []
            ],
            # number_of returns 2; this doesn't match 3
            [
                [('number_of', "river", 3)],
                []
            ],
            # number_of returns 2; and it matches
            [
                [('number_of', "river", 2)],
                [{}]
            ],
        ]

        for test in tests:
            question, answer = test
            result = solver.solve(question)
            self.assertEqual(answer, result)
