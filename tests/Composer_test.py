import unittest

from richard.core.Model import Model
from richard.core.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.core.constants import E1, E2, Body, Range
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.parser.helper.grammar_functions import apply
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.type.SemanticTemplate import SemanticTemplate

class TestComposer(unittest.TestCase):

    def test_missing_sem(self):
        grammar = [
            { "syn": "s(E1) -> proper_noun(E1) verb(V)", "sem": lambda proper_noun, verb: proper_noun + verb },
            { "syn": "proper_noun(E1) -> 'mary'" },
            { "syn": "verb(E1) -> 'walks'" },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
        ])

        exception_occurred = False
        try:
            pipeline.enter(SentenceRequest("Mary walks"))
        except Exception as e:
            self.assertEqual(str(e), "Rule 'proper_noun(E1) -> 'mary'' is missing key 'sem'")
            exception_occurred = True

        self.assertEqual(exception_occurred, True)


    def test_variable_unification(self):

        grammar = [
            { "syn": "s(E1) -> np(E1) vp(E1)", "sem": lambda np, vp: apply(np, vp)},
            { "syn": "vp(E1) -> verb(E1, E2) np(E2)", "sem": lambda verb, np: apply(np, verb) },
            { "syn": "verb(E1, E2) -> 'flows' 'to'", "sem": lambda: [('flows', E1, E2)] },
            { "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar: SemanticTemplate([Body], apply(det, nbar, Body)) },
            { "syn": "det(E1) -> 'the'", "sem": lambda: SemanticTemplate([Range, Body], Range + Body) },
            { "syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun },
            { "syn": "noun(E1) -> 'river'", "sem": lambda: [('river', E1)] },
            { "syn": "noun(E1) -> 'sea'", "sem": lambda: [('sea', E1)] },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
        ])

        request = SentenceRequest("The river flows to the sea")
        pipeline.enter(request)
        composition = composer.get_composition(request)
        self.assertEqual(str(composition.get_semantics_last_iteration()), "[('river', $1), ('sea', $2), ('flows', $1, $2)]")


    def test_special_category(self):

        grammar = [
            { "syn": "s(V) -> np(E1) 'sleeps'", "sem": lambda np: np },
            { "syn": "np(E1) -> proper_noun(E1)", "sem": lambda proper_noun: proper_noun },
            { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
        ])

        request = SentenceRequest("John sleeps")
        pipeline.enter(request)

        tree = parser.get_tree(request)
        self.assertEqual(tree.inline_str(), "s(np(proper_noun(token 'John')) sleeps 'sleeps')")
        composition = composer.get_composition(request)
        self.assertEqual(str(composition.get_semantics_last_iteration()), "John")


    def test_multiple_return_variables(self):

        grammar = [
            { "syn": "s(E1, E2) -> np(E1) vp(E2)", "sem": lambda np, vp: np + vp },
            { "syn": "np(E1) -> 'john'", "sem": lambda: 'john' },
            { "syn": "vp(E1) -> 'sleeps'", "sem": lambda: 'sleeps' },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
        ])

        request = SentenceRequest("John sleeps")
        pipeline.enter(request)

        composition = composer.get_composition(request)
        self.assertEqual(composition.return_variables, ["$1", "$2"])

