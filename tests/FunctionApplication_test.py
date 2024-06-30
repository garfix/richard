import unittest

from richard.Pipeline import Pipeline
from richard.block.FindAll import FindAll
from richard.block.FindOne import FindOne
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer


class TestFunctionApplication(unittest.TestCase):
    """
    This simple method of semantics by function application is only useful for mathematical expressions.
    The example was found here: https://github.com/percyliang/sempre/blob/master/TUTORIAL.md
    """

    def test_find_all(self):

        grammar = [
            { "syn": "s(E1) -> 'what' 'is' term(E1)", "sem": lambda term: term },
            { "syn": "s(E1) -> 'calculate' term(E1)", "sem": lambda term: term },
            { 
                "syn": "term(E1) -> term(E2) operator(E3) term(E4)", 
                "sem": lambda term1, operator, term2: operator(term1, term2)
            },
            { "syn": "operator(E1) -> 'plus'",  "sem": lambda: lambda a, b: a + b },
            { "syn": "operator(E1) -> 'minus'", "sem": lambda: lambda a, b: a - b },
            { "syn": "operator(E1) -> 'times'",  "sem": lambda: lambda a, b: a * b },
            { "syn": "operator(E1) -> 'divided' 'by'", "sem": lambda: lambda a, b: a / b },
            { "syn": "term(E1) -> 'one'", "sem": lambda: 1 },
            { "syn": "term(E1) -> 'two'", "sem": lambda: 2 },
            { "syn": "term(E1) -> 'three'", "sem": lambda: 3 },
            { "syn": "term(E1) -> 'four'", "sem": lambda: 4 },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer)
        ])

        request = SentenceRequest("What is three plus four")
        pipeline.enter(request)
        results = composer.get_tuples(request)
        self.assertEqual(results, 7)
        
        # test find_all
        # test ambiguous sentence with 2 readings (that exposed an error in the parser, now solved)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindAll(parser),
            FindAll(composer)
        ])
        request = SentenceRequest("Calculate three plus four times two")
        pipeline.enter(request)

        self.assertEqual(request.get_alternative_products(composer), [14, 11])
