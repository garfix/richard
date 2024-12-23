import sqlite3
import unittest

from richard.core.Model import Model
from richard.core.constants import E1, E2
from richard.data_source.Sqlite3DataSource import Sqlite3DataSource
from richard.entity.Relation import Relation
from richard.entity.ResultIterator import ResultIterator
from richard.interface.SomeDataSource import SomeDataSource
from richard.core.Solver import Solver
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext


class TestResultIterator(ResultIterator):
    def __next__(self):
        raise Exception("As this iterator is only called using 'count', its individual items should not be accessed")


class TestModule(SomeModule):
    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("river", query_function=self.simple_entity))
        self.add_relation(Relation("country", query_function=self.simple_entity))
        self.add_relation(Relation("contains", query_function=self.contains))
        self.add_relation(Relation("number_of", query_function=self.number_of))
        self.add_relation(Relation("return_iterator", query_function=self.return_iterator))


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


    def return_iterator(self, values: list, context: ExecutionContext) -> list[list]:
        return TestResultIterator([None, 2], 100000000)


class TestSolver(unittest.TestCase):

    def test_solver(self):

        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()
        data_source = Sqlite3DataSource(connection)

        # note: same entity may have multiple names
        cursor.execute("CREATE TABLE river (id TEXT)")
        cursor.execute("CREATE TABLE country (id TEXT)")
        cursor.execute("CREATE TABLE contains (country TEXT, river TEXT)")

        data_source.insert('river', ['id'], ['amazon'])
        data_source.insert('river', ['id'], ['brahmaputra'])

        data_source.insert('country', ['id'], ['brasil'])
        data_source.insert('country', ['id'], ['india'])

        data_source.insert('contains', ['country', 'river'], ['brasil', 'amazon'])
        data_source.insert('contains', ['country', 'river'], ['india', 'brahmaputra'])


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
            # counting with a ResultIterator
            [
                [('count', E1, [('return_iterator',)])],
                [{'E1': 100000000}]
            ],
        ]

        for test in tests:
            question, answer = test
            result = solver.solve(question)
            self.assertEqual(answer, result)
