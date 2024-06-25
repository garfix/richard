import unittest

from richard.Solver import Solver
from richard.ModelAdapter import ModelAdapter
from richard.Model import Model
from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.entity.Entity import Entity
from richard.entity.Relation import Relation
from richard.entity.Variable import Variable
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeSolver import SomeSolver
from richard.store.Record import Record
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.TupleComposer import TupleComposer
from richard.processor.semantic_executor.TupleExecutor import TupleExecutor
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.semantics.commands import dehydrate_values
from richard.store.MemoryDb import MemoryDb
from richard.type.Simple import Simple


E1 = Variable('E1')
E2 = Variable('E2')
Result = Variable('Result')
Range = Variable('Range')


class TestAdapter(ModelAdapter):
    ds: SomeDataSource

    def __init__(self, data_source: SomeDataSource) -> None:

        self.ds = data_source

        super().__init__(
            relations=[
                Relation("has_child", ['parent', 'child']),
                Relation("parent", ['parent']),
                Relation("child", ['child']),
            ], 
        )


    def interpret_relation(self, relation: str, model_values: list, solver: SomeSolver) -> list[list]:

        values = dehydrate_values(model_values)

        # print(model_values)

        if relation == "has_child":
            return self.ds.select("has_child", ["parent", "child"], values)
        elif relation == "parent":
            return self.ds.select("has_child", ["parent"], values)
        elif relation == "child":
            return self.ds.select("has_child", ["child"], values)
        if relation == "have" and model_values[0].entity == "parent" and model_values[1].entity == "child":
            return self.ds.select("has_child", ["parent", "child"], values)
        return []


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
        model = Model(TestAdapter(data_source), [])

        grammar = [
            { 
                "syn": "s(V1) -> np(E1) vp_no_sub(E1)", 
                "sem": lambda np, vp_no_sub: [('check', np, vp_no_sub)]
            },
            { 
                "syn": "vp_no_sub(E1) -> 'has' np(E2)", 
                "sem": lambda np: [('check', np, [('have', E1, E2)])] 
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
            { "syn": "aux(V1) -> 'has'", "sem": lambda: None },
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
        result = pipeline.enter(request)
        # if not result.error_code == "":
        #         print(result.error_code, result.error_args) 
        results = executor.get_results(request)
        self.assertEqual(len(results), 3)

        request = SentenceRequest("Every parent has three children")
        pipeline.enter(request)
        results = executor.get_results(request)
        self.assertEqual(len(results), 0)
