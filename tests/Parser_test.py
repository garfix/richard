import unittest

from lib.entity.Pipeline import Pipeline
from lib.entity.SentenceRequest import SentenceRequest
from lib.processor.parser.BasicParser import BasicParser
from lib.processor.tokenizer.BasicTokenizer import BasicTokenizer

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

        tree = request.get_current_product(parser)

        print(tree)
    