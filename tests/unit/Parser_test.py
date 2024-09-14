import unittest

from richard.core.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParserProduct import BasicParserProduct
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer

class TestParser(unittest.TestCase):

    def test_parser_process(self):

        grammar = [
            { "syn": "s(V) -> np(E1) vp(V, E1)" },
            { "syn": "vp(V, E1) -> verb(V) np(E1)" },
            { "syn": "np(E1) -> noun(E1)" },
            { "syn": "noun(E1) -> proper_noun(E1)" },
            { "syn": "proper_noun(E1) -> 'john'" },
            { "syn": "proper_noun(E1) -> 'mary'" },
            { "syn": "verb(V) -> 'loves'" },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser)
        ])

        request = SentenceRequest("John loves Mary")
        parse_tree = pipeline.enter(request)
        self.assertEqual(parse_tree.inline_str(), "s(np(noun(proper_noun(john 'John'))) vp(verb(loves 'loves') np(noun(proper_noun(mary 'Mary')))))")


    def test_quote(self):

        grammar = [
            { "syn": "s(V) -> np(E1) '\\'' 's' np(E2)" },
            { "syn": "np(E1) -> 'john'" },
            { "syn": "np(E1) -> 'shoe'" },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser)
        ])

        request = SentenceRequest("John's shoe")
        parse_tree = pipeline.enter(request)

        self.assertEqual(parse_tree.inline_str(), "s(np(john 'John') ' ''' s 's' np(shoe 'shoe'))")


    def test_syntax_error(self):
        grammar = [
            { "syn": "s(V) => proper_noun(E1) verb(V)" },
            { "syn": "proper_noun(E1) -> 'mary'" },
            { "syn": "verb(V) -> 'walks'" },
        ]

        tokenizer = BasicTokenizer()

        try:
            parser = BasicParser(grammar, tokenizer)
        except Exception as e:
            self.assertEqual(str(e), "Missing -> operator in 'syn' value: s(V) => proper_noun(E1) verb(V)")
