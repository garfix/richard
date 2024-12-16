import unittest

from richard.core.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser

class TestParser(unittest.TestCase):

    def test_parser_process(self):

        simple_grammar = [
            { "syn": "s(V) -> np(E1) vp(V, E1)" },
            { "syn": "vp(V, E1) -> verb(V) np(E1)" },
            { "syn": "np(E1) -> noun(E1)" },
            { "syn": "noun(E1) -> proper_noun(E1)" },
            { "syn": "proper_noun(E1) -> 'john'" },
            { "syn": "proper_noun(E1) -> 'mary'" },
            { "syn": "verb(V) -> 'loves'" },
        ]

        grammar = SimpleGrammarRulesParser().parse(simple_grammar)
        parser = BasicParser(grammar)

        pipeline = Pipeline([
            FindOne(parser)
        ])

        request = SentenceRequest("John loves Mary")
        parse_tree = pipeline.enter(request)
        self.assertEqual(parse_tree.inline_str(), "s(np(noun(proper_noun(john 'john'))) vp(verb(loves 'loves') np(noun(proper_noun(mary 'mary')))))")


    def test_quote(self):

        simple_grammar = [
            { "syn": "s(V) -> np(E1)+'\\''+'s' np(E2)" },
            { "syn": "np(E1) -> 'john'" },
            { "syn": "np(E1) -> 'shoe'" },
        ]

        grammar = SimpleGrammarRulesParser().parse(simple_grammar)
        parser = BasicParser(grammar)

        pipeline = Pipeline([
            FindOne(parser)
        ])

        request = SentenceRequest("John's shoe")
        parse_tree = pipeline.enter(request)

        self.assertEqual(parse_tree.inline_str(), "s(np(john 'john') ' ''' s 's' np(shoe 'shoe'))")


    def test_syntax_error(self):
        simple_grammar = [
            { "syn": "s(V) => proper_noun(E1) verb(V)" },
            { "syn": "proper_noun(E1) -> 'mary'" },
            { "syn": "verb(V) -> 'walks'" },
        ]

        try:
            grammar = SimpleGrammarRulesParser().parse(simple_grammar)
            parser = BasicParser(grammar)
        except Exception as e:
            self.assertEqual(str(e), "Missing -> operator in 'syn' value: s(V) => proper_noun(E1) verb(V)")
