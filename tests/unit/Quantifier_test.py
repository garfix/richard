import sqlite3
import unittest

from richard.block.TryFirst import TryFirst
from richard.core.Model import Model
from richard.core.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.core.constants import E1, E2, Body, Range
from richard.data_source.Sqlite3DataSource import Sqlite3DataSource
from richard.entity.Relation import Relation
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.parser.helper.grammar_functions import apply
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.type.ExecutionContext import ExecutionContext
from richard.type.SemanticTemplate import SemanticTemplate


class TestModule(SomeModule):
    ds: SomeDataSource

    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("parent", query_function=self.parent))
        self.add_relation(Relation("child", query_function=self.child))
        self.add_relation(Relation("have", query_function=self.have))


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

        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()
        data_source = Sqlite3DataSource(connection)

        # note: same entity may have multiple names
        cursor.execute("CREATE TABLE has_child (parent TEXT, child TEXT)")

        data_source.insert('has_child', ['parent', 'child'], ['mary', 'lucy'])
        data_source.insert('has_child', ['parent', 'child'], ['mary', 'bonny'])
        data_source.insert('has_child', ['parent', 'child'], ['barbara', 'john'])
        data_source.insert('has_child', ['parent', 'child'], ['barbara', 'chuck'])
        data_source.insert('has_child', ['parent', 'child'], ['william', 'oswald'])
        data_source.insert('has_child', ['parent', 'child'], ['william', 'bertrand'])

        model = Model([TestModule(data_source)])

        simple_grammar = [
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

        grammar = SimpleGrammarRulesParser().parse(simple_grammar)
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)
        executor = AtomExecutor(composer, model)

        pipeline = Pipeline([
            FindOne(parser),
            TryFirst(composer),
            TryFirst(executor)
        ])

        request = SentenceRequest("Every parent has two children")
        bindings = pipeline.enter(request)
        self.assertEqual(len(bindings), 3)

        request = SentenceRequest("Every parent has three children")
        bindings = pipeline.enter(request)
        self.assertEqual(len(bindings), 0)
