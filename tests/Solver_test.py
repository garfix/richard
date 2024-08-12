import unittest

from richard.Model import Model
from richard.constants import E1, E2, IGNORED
from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.entity.Relation import Relation
from richard.entity.Instance import Instance
from richard.interface import SomeSolver
from richard.interface.SomeDataSource import SomeDataSource
from richard.Solver import Solver
from richard.interface.SomeModule import SomeModule
from richard.store.MemoryDb import MemoryDb
from richard.store.Record import Record
from richard.type.ExecutionContext import ExecutionContext


class TestModule(SomeModule):
    def __init__(self, data_source: SomeDataSource) -> None:

        self.ds = data_source

    def get_relations(self):
        return {
            "river": Relation(self.simple_entity),
            "country": Relation(self.simple_entity),
            "contains": Relation(self.contains),
        }
    
    
    def simple_entity(self, values: list, context: ExecutionContext) -> list[list]:
        db_values = self.dehydrate_values(values)
        out_types = [context.predicate]
        out_values = self.ds.select(context.predicate, ['id'], db_values)
        return self.hydrate_values(out_values, out_types)
    
    
    def contains(self, values: list, context: ExecutionContext) -> list[list]:
        db_values = self.dehydrate_values(values)
        out_types = ["country", "river"]
        out_values = self.ds.select("contains", ['country', 'river'], db_values)
        return self.hydrate_values(out_values, out_types)


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
                [{'E1': Instance('river', 'amazon')}, {'E1': Instance('river', 'brahmaputra')}]
            ],
            [
                [('river', E1), ('contains', Instance('country', 'india'), E1)], 
                [{'E1': Instance('river', 'brahmaputra')}]
            ],
            [
                [('contains', E1, E2), ('country', E1)], 
                [{'E1': Instance('country', 'brasil'), 'E2': Instance('river', 'amazon')}, 
                 {'E1': Instance('country', 'india'), 'E2': Instance('river', 'brahmaputra')}]
            ],
            [
                [('contains', E1, E1)], 
                []
            ],
        ]

        for test in tests:
            question, answer = test
            result = solver.solve(question, {})
            self.assertEqual(answer, result)
            