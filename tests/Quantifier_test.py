import unittest

from richard.core.Model import Model
from richard.core.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.core.constants import E1, E2, Body, Range
from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.entity.Relation import Relation
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.processor.parser.helper.grammar_functions import apply
from richard.processor.semantic_executor.AtomExecutorProduct import AtomExecutorProduct
from richard.store.Record import Record
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.store.MemoryDb import MemoryDb
from richard.type.ExecutionContext import ExecutionContext
from richard.type.SemanticTemplate import SemanticTemplate


class TestModule(SomeModule):
    ds: SomeDataSource

    def __init__(self, data_source: SomeDataSource) -> None:
        self.ds = data_source


    def get_relations(self):
        return {
            "parent": Relation(query_function=self.parent),
            "child": Relation(query_function=self.child),
            "have": Relation(query_function=self.have),
        }


    def parent(self, values: list, context: ExecutionContext) -> list[list]:
        out_values = self.ds.select("has_child", ["parent"], values)
        return out_values


    def child(self, values: list, context: ExecutionContext) -> list[list]:
        out_values = self.ds.select("has_child", ["child"], values)
        return out_values


    def have(self, values: list, context: ExecutionContext) -> list[list]:
        out_values = self.ds.select("has_child", ["parent", "child"], values)
        return out_values


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
                "sem": lambda np, vp_no_sub: apply(np, vp_no_sub)
            },
            {
                "syn": "vp_no_sub(E1) -> tv(E1, E2) np(E2)",
                "sem": lambda tv, np: apply(np, tv)
            },
            {
                "syn": "tv(E1, E2) -> 'has'",
                "sem": lambda: [('have', E1, E2)]
            },
            {
                "syn": "np(E1) -> det(E1) nbar(E1)",
                "sem": lambda det, nbar: SemanticTemplate([Body], apply(det, nbar, Body))
            },
            {
                "syn": "nbar(E1) -> noun(E1)",
                "sem": lambda noun: noun
            },
            {
                "syn": "det(E1) -> 'every'",
                "sem": lambda: SemanticTemplate([Range, Body], [('all', E1, Range, Body)])
            },
            {
                "syn": "det(E1) -> number(E1)",
                "sem": lambda number: SemanticTemplate([Range, Body], [('det_equals', Range + Body, number)])
            },
            { "syn": "number(D1) -> 'two'", "sem": lambda: 2 },
            { "syn": "number(D1) -> 'three'", "sem": lambda: 3 },
            { "syn": "noun(E1) -> 'parent'", "sem": lambda: [('parent', E1)] },
            { "syn": "noun(E1) -> 'children'", "sem": lambda: [('child', E1)] },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)
        executor = AtomExecutor(composer, model)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
            FindOne(executor)
        ])

        request = SentenceRequest("Every parent has two children")
        results: AtomExecutorProduct = pipeline.enter(request)
        self.assertEqual(len(results.bindings), 3)

        request = SentenceRequest("Every parent has three children")
        results: AtomExecutorProduct = pipeline.enter(request)
        self.assertEqual(len(results.bindings), 0)
