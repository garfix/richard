import unittest

from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer

class TestParser(unittest.TestCase):
   
    def test_parser_process(self):

        grammar = [
            { "syn": "s -> np vp" },
            { "syn": "vp -> verb np" },
            { "syn": "np -> noun" },
            { "syn": "noun -> proper_noun" },
            { "syn": "proper_noun -> 'john'" },
            { "syn": "proper_noun -> 'mary'" },
            { "syn": "verb -> 'loves'" },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser)
        ])

        request = SentenceRequest("John loves Mary")
        pipeline.enter(request)

        tree = parser.get_tree(request)
        self.assertEqual(tree.inline_str(), "s(np(noun(proper_noun(john 'John'))) vp(verb(loves 'loves') np(noun(proper_noun(mary 'Mary')))))")
    

    def test_syntax_error(self):
        grammar = [
            { "syn": "s => proper_noun verb" },
            { "syn": "proper_noun -> 'mary'" },
            { "syn": "verb -> 'walks'" },
        ]

        tokenizer = BasicTokenizer()

        try:
            parser = BasicParser(grammar, tokenizer)
        except Exception as e:
            self.assertEqual(str(e), "Could not parse 'syn' value: s => proper_noun verb")
