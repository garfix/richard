import unittest

from richard.Solver import Solver
from richard.Model import Model
from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.entity.Variable import Variable
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.interface.SomeSolver import SomeSolver
from richard.store.Record import Record
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.TupleComposer import TupleComposer
from richard.processor.semantic_executor.TupleExecutor import TupleExecutor
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.store.MemoryDb import MemoryDb


E1 = Variable('E1')
E2 = Variable('E2')
Result = Variable('Result')
Range = Variable('Range')


class TestModule(SomeModule):
    ds: SomeDataSource

    def __init__(self, data_source: SomeDataSource) -> None:
        self.ds = data_source


    def get_relations(self):
        return [
            "parent", 
            "child",
            "have",
        ]


    def interpret_relation(self, relation: str, db_values: list, in_types: list[str], solver: SomeSolver, binding: dict) -> list[list]:

        if relation == "parent":
            out_types = ["parent"]
            db_values = self.ds.select("has_child", ["parent"], db_values)
        elif relation == "child":
            out_types = ["child"]
            db_values = self.ds.select("has_child", ["child"], db_values)
        elif relation == "have" and in_types[0] == "parent" and in_types[1] == "child":
            out_types = ["parent", "child"]
            db_values = self.ds.select("has_child", ["parent", "child"], db_values)
        else:
            out_types = []
            db_values = []
      
        return db_values, out_types


class TestQuantification(unittest.TestCase):
   
    def test_quantification(self):

        db = MemoryDb()
        db.insert(Record('has_child', {'parent': 'mary', 'child': 'lucy'}))
        db.insert(Record('has_child', {'parent': 'mary', 'child': 'bonny'}))
        db.insert(Record('has_child', {'parent': 'barbara', 'child': 'john'}))
        db.insert(Record('has_child', {'parent': 'barbara', 'child': 'chuck'}))
        db.insert(Record('has_child', {'parent': 'william', 'child': 'oswald'}))
        db.insert(Record('has_child', {'parent': 'william', 'child': 'bertrand'}))

        data_source = MemoryDbDataSource(db)
        model = Model([TestModule(data_source)])

        grammar = [
            { 
                "syn": "s(V1) -> np(E1) vp_no_sub(E1)", 
                "sem": lambda np, vp_no_sub: [('check', np, vp_no_sub)]
            },
            { 
                "syn": "vp_no_sub(E1) -> tv(E1, E2) np(E2)", 
                "sem": lambda tv, np: [('check', np, tv)] 
            },
            { 
                "syn": "tv(E1, E2) -> 'has'", 
                "sem": lambda: [('have', E1, E2)] 
            },
            { 
                "syn": "np(E1) -> det(D1) nbar(E1)", 
                "sem": lambda det, nbar: ('quant', E1, det, nbar) 
            },
            { 
                "syn": "nbar(E1) -> noun(E1)", 
                "sem": lambda noun: noun 
            },
            { 
                "syn": "det(D1) -> 'every'", 
                "sem": lambda: ('determiner', Result, Range, [('==', Result, Range)])
            },
            { 
                "syn": "det(D1) -> number(D1)", 
                "sem": lambda number: ('determiner', Result, Range, [('==', Result, number)])     
            },
            { "syn": "number(D1) -> 'two'", "sem": lambda: 2 },
            { "syn": "number(D1) -> 'three'", "sem": lambda: 3 },
            { "syn": "noun(E1) -> 'parent'", "sem": lambda: [('parent', E1)] },
            { "syn": "noun(E1) -> 'children'", "sem": lambda: [('child', E1)] },
        ]

        solver = Solver(model)
        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = TupleComposer(parser)
        executor = TupleExecutor(composer, solver)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
            FindOne(executor)
        ])

        request = SentenceRequest("Every parent has two children")
        pipeline.enter(request)
        results = executor.get_results(request)
        self.assertEqual(len(results), 3)

        request = SentenceRequest("Every parent has three children")
        pipeline.enter(request)
        results = executor.get_results(request)
        self.assertEqual(len(results), 0)
