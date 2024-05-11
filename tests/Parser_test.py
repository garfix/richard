import unittest

from richard.Pipeline import Pipeline
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
            tokenizer,
            parser
        ])

        request = SentenceRequest("John loves Mary")
        pipeline.enter(request)

        tree = parser.get_tree(request)
        self.assertEqual(tree.inline_str(), "s(np(noun(proper_noun(john 'John'))) vp(verb(loves 'loves') np(noun(proper_noun(mary 'Mary')))))")
    