import unittest

from lib.entity.Pipeline import Pipeline
from lib.entity.Request import Request
from lib.parser.ParserProcess import ParserProcess

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
        parser = ParserProcess(grammar)

        pipeline = Pipeline([
            parser
        ])

        request = Request("John loves Mary")

        pipeline.enter(request)

        tree = request.get_alternative(parser)

        print(tree)
    