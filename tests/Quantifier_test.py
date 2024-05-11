import unittest

from lib.Pipeline import Pipeline
from lib.entity.Record import Record
from lib.entity.SentenceRequest import SentenceRequest
from lib.processor.parser.BasicParser import BasicParser
from lib.processor.semantic_composer.SemanticComposer import SemanticComposer
from lib.processor.semantic_executor.SemanticExecutor import SemanticExecutor
from lib.processor.tokenizer.BasicTokenizer import BasicTokenizer
from lib.semantics.commands import find
from lib.store.MemoryDb import MemoryDb


class TestQuantifier(unittest.TestCase):
   
    def test_quantifier(self):

        db = MemoryDb()
        db.assert_record(Record('has_child', {'parent': 'mary', 'child': 'lucy'}))
        db.assert_record(Record('has_child', {'parent': 'mary', 'child': 'bonny'}))
        db.assert_record(Record('has_child', {'parent': 'barbara', 'child': 'john'}))
        db.assert_record(Record('has_child', {'parent': 'barbara', 'child': 'chuck'}))
        db.assert_record(Record('has_child', {'parent': 'william', 'child': 'oswald'}))
        db.assert_record(Record('has_child', {'parent': 'william', 'child': 'bertrand'}))

        grammar = [
            { 
                "syn": "s -> np vp_no_sub", 
                "sem": lambda np, vp_no_sub: lambda: find(np(), vp_no_sub) 
            },
            { 
                "syn": "vp_no_sub -> aux qp child", 
                "sem": lambda aux, qp, parent:
                        lambda sub: find(
                            (qp, parent),
                            lambda obj: db.match(Record('has_child', {'parent': sub, 'child': obj})))
            },
            { 
                "syn": "np -> qp nbar", 
                "sem": lambda qp, nbar:  lambda: (qp, nbar) 
            },
            { 
                "syn": "qp -> det", 
                "sem": lambda det: lambda result, range: det(result, range) 
            },
            { "syn": "nbar -> noun", "sem": lambda noun: lambda: noun() },
            { 
                "syn": "det -> 'every'", 
                "sem": lambda: lambda result, range: result == range 
            },
            { 
                "syn": "det -> number", 
                "sem": lambda number: lambda result, range: result == number() 
            },
            { "syn": "number -> 'two'", "sem": lambda: lambda: 2 },
            { "syn": "number -> 'three'", "sem": lambda: lambda: 3 },
            { "syn": "noun -> 'parent'", "sem": lambda: lambda: db.match(Record('has_child')).field('parent') },
            { "syn": "child -> 'children'", "sem": lambda: lambda: db.match(Record('has_child')).field('child') },
            { "syn": "aux -> 'has'", "sem": lambda: lambda: None },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)
        executor = SemanticExecutor(composer)

        pipeline = Pipeline([
            tokenizer,
            parser,
            composer,
            executor
        ])

        request = SentenceRequest("Every parent has two children")
        pipeline.enter(request)
        results = executor.get_results(request)
        self.assertEqual(len(results), 3)

        request = SentenceRequest("Every parent has three children")
        pipeline.enter(request)
        results = executor.get_results(request)
        self.assertEqual(len(results), 0)
