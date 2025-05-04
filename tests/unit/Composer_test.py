import re
import unittest

from richard.core.System import System
from richard.block.FindOne import FindOne
from richard.core.constants import E1, E2, Body, Range
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParserProduct import BasicParserProduct
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.parser.helper.grammar_functions import apply
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.type.SemanticFunction import SemanticFunction

class TestComposer(unittest.TestCase):

    def test_missing_sem(self):
        simple_grammar = [
            { "syn": "s(E1) -> proper_noun(E1) verb(V)", "sem": lambda proper_noun, verb: proper_noun + verb },
            { "syn": "proper_noun(E1) -> 'mary'" },
            { "syn": "verb(E1) -> 'walks'" },
        ]

        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)

        system = System(
            input_pipeline=[
                FindOne(parser),
                FindOne(composer),
            ]
        )

        exception_occurred = False
        try:
            system.enter(SentenceRequest("Mary walks"))
        except Exception as e:
            self.assertEqual(str(e), "Rule 'proper_noun(E1) -> 'mary'' is missing key 'sem'")
            exception_occurred = True

        self.assertEqual(exception_occurred, True)


    def test_variable_unification(self):

        simple_grammar = [
            { "syn": "s(E1) -> np(E1) vp(E1)", "sem": lambda np, vp: apply(np, vp)},
            { "syn": "vp(E1) -> verb(E1, E2) np(E2)", "sem": lambda verb, np: apply(np, verb) },
            { "syn": "verb(E1, E2) -> 'flows' 'to'", "sem": lambda: [('flows', E1, E2)] },
            { "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar: SemanticFunction([Body], apply(det, nbar, Body)) },
            { "syn": "det(E1) -> 'the'", "sem": lambda: SemanticFunction([Range, Body], Range + Body) },
            { "syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun },
            { "syn": "noun(E1) -> 'river'", "sem": lambda: [('river', E1)] },
            { "syn": "noun(E1) -> 'sea'", "sem": lambda: [('sea', E1)] },
        ]

        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)

        system = System(
            input_pipeline=[
                FindOne(parser),
                FindOne(composer),
            ]
        )

        request = SentenceRequest("The river flows to the sea")
        semantics = system.enter(request)
        self.assertEqual(str(semantics), "[('river', $1), ('sea', $2), ('flows', $1, $2)]")


    def test_special_category(self):

        simple_grammar = [
            { "syn": "s(V) -> np(E1) 'sleeps'", "sem": lambda np: np },
            { "syn": "np(E1) -> proper_noun(E1)", "sem": lambda proper_noun: proper_noun },
            { "syn": "proper_noun(E1) -> /\w+/", "sem": lambda token: token },
            { "syn": "proper_noun(E1) -> /\w+ \w+/", "sem": lambda token: token },
        ]

        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)

        system = System(
            input_pipeline=[
                FindOne(parser),
                FindOne(composer),
            ]
        )

        # basic

        request = SentenceRequest("John sleeps")
        semantics = system.enter(request)

        product: BasicParserProduct = request.get_current_product(parser)
        self.assertEqual(product.parse_tree.inline_str(), "s(np(proper_noun(\w+ 'John')) sleeps 'sleeps')")
        self.assertEqual(str(semantics), "John")

        # two tokens

        request = SentenceRequest("John Walker sleeps")
        semantics = system.enter(request)
        self.assertEqual(str(semantics), "John Walker")


    def test_multiple_return_variables(self):

        simple_grammar = [
            { "syn": "s(E1, E2) -> np(E1) vp(E2)", "sem": lambda np, vp: np + vp },
            { "syn": "np(E1) -> 'john'", "sem": lambda: 'john' },
            { "syn": "vp(E1) -> 'sleeps'", "sem": lambda: 'sleeps' },
        ]

        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)

        system = System(
            input_pipeline=[
                FindOne(parser),
                FindOne(composer),
            ]
        )

        request = SentenceRequest("John sleeps")
        system.enter(request)
        composition = request.get_current_product(composer)
        self.assertEqual(composition.return_variables, ["$1", "$2"])


    def test_regexp(self):

        simple_grammar = [
            { "syn": "s(V) -> 'does' np(E1) 'sleep'~'?'", "sem": lambda np: np },
            { "syn": "np(E1) -> proper_noun(E1)", "sem": lambda proper_noun: proper_noun },
            { "syn": "proper_noun(E1) -> /\w+/", "sem": lambda token: token },
        ]

        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)

        system = System(
            input_pipeline=[
                FindOne(parser),
                FindOne(composer),
            ]
        )

        # basic

        request = SentenceRequest("Does John sleep?")
        semantics = system.enter(request)

        product: BasicParserProduct = request.get_current_product(parser)
        self.assertEqual(str(semantics), "John")
