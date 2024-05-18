import unittest

from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer

class TestComposer(unittest.TestCase):
   
    def test_missing_sem(self):
        grammar = [
            { "syn": "s -> proper_noun verb", "sem": lambda proper_noun, verb: "not a function" },
            { "syn": "proper_noun -> 'mary'" },
            { "syn": "verb -> 'walks'" },
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
            self.assertEqual(str(e), "Rule 'proper_noun -> 'mary'' is missing key 'sem'")
            exception_occurred = True
        
        self.assertEqual(exception_occurred, True)


    def test_inner_not_a_function(self):
        grammar = [
            { "syn": "s -> proper_noun verb", "sem": lambda proper_noun, verb: "this is not a function" },
            { "syn": "proper_noun -> 'mary'", "sem": lambda: lambda: None },
            { "syn": "verb -> 'walks'", "sem": lambda: lambda: None },
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
            self.assertEqual(str(e), "Rule 's -> proper_noun verb' key 'sem' does not return a function")
            exception_occurred = True
        
        self.assertEqual(exception_occurred, True)


    def test_outer_not_a_function(self):
        grammar = [
            { "syn": "s -> proper_noun verb", "sem": "this is not a function" },
            { "syn": "proper_noun -> 'mary'", "sem": lambda: lambda: None },
            { "syn": "verb -> 'walks'", "sem": lambda: lambda: None },
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
            self.assertEqual(str(e), "Rule 's -> proper_noun verb' key 'sem' is not a function")
            exception_occurred = True
        
        self.assertEqual(exception_occurred, True)
