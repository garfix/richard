import unittest

from richard.Model import Model
from richard.ModelAdapter import ModelAdapter
from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.entity.Instance import Instance
from richard.entity.Relation import Relation
from richard.entity.Variable import Variable
from richard.interface.SomeDataSource import SomeDataSource
from richard.Solver import Solver
from richard.semantics.commands import dehydrate_values
from richard.store.MemoryDb import MemoryDb
from richard.store.Record import Record
from richard.type.Simple import Simple

E1 = Variable('E1')
E2 = Variable('E2')
E3 = Variable('E3')
E4 = Variable('E4')


class TestAdapter(ModelAdapter):
    def __init__(self, data_source: SomeDataSource) -> None:

        self.ds = data_source

        super().__init__(
            relations=[
                Relation("river", ["river"]),
                Relation("country", ["country"]),
                Relation("contains", ["country", "river"]),
            ], 
        )


    def interpret_relation(self, relation_name: str, model_values: list[Simple]) -> list[list[Simple]]:
        values = dehydrate_values(model_values)
        if relation_name == "river":
            out_values = self.ds.select("river", ['id'], values)
        elif relation_name == "country":
            out_values = self.ds.select("country", ['id'], values)
        elif relation_name == "contains":
            out_values = self.ds.select("contains", ['country', 'river'], values)
        else:
            out_values = []

        # return self.hydrate


    def interpret_entity(self, entity_name: str) -> list[Simple]:
        return []
    

    def interpret_attribute(self, entity_name: str, attribute_name: str, values: list[Simple]) -> list[Simple]:
        return []
    
    
    def interpret_modifier(self, entity_name: str, modifier_name: str, value: Simple) -> list[Simple]:
        return []


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
        model = Model(TestAdapter(data_source))
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
            print()
            print(question)
            result = solver.solve(question)
            print(result)
            self.assertEqual(answer, result)
            