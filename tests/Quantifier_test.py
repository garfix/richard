import unittest

from richard.Model import Model
from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.entity.Entity import Entity
from richard.entity.Relation import Relation
from richard.store.Record import Record
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.SemanticExecutor import SemanticExecutor
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.semantics.commands import filter, dnp
from richard.store.MemoryDb import MemoryDb


class TestFind(unittest.TestCase):
   
    def test_find(self):

        db = MemoryDb()
        db.insert(Record('has_child', {'parent': 'mary', 'child': 'lucy'}))
        db.insert(Record('has_child', {'parent': 'mary', 'child': 'bonny'}))
        db.insert(Record('has_child', {'parent': 'barbara', 'child': 'john'}))
        db.insert(Record('has_child', {'parent': 'barbara', 'child': 'chuck'}))
        db.insert(Record('has_child', {'parent': 'william', 'child': 'oswald'}))
        db.insert(Record('has_child', {'parent': 'william', 'child': 'bertrand'}))

        model = Model([
            Entity("parent", lambda: db.select(Record('has_child')).field('parent')),
            Entity("child", lambda: db.select(Record('has_child')).field('child')),
        ], [
            Relation("has_child", ['parent', 'child'], lambda parent, child: db.select(Record('has_child', {'parent': parent, 'child': child}))),
        ])

        grammar = [
            { 
                "syn": "s -> np vp_no_sub", 
                "sem": lambda np, vp_no_sub: lambda: filter(np(), vp_no_sub) 
            },
            { 
                "syn": "vp_no_sub -> aux det child", 
                "sem": lambda aux, det, child:
                        lambda subject: filter(
                            dnp(det, child),
                            lambda object: model.relation_exists('has_child', [subject, object]))
            },
            { 
                "syn": "np -> det nbar", 
                "sem": lambda det, nbar:  lambda: dnp(det, nbar) 
            },
            { 
                "syn": "det -> quantifier", 
                "sem": lambda quantifier: lambda result, range: quantifier(result, range) 
            },
            { "syn": "nbar -> noun", "sem": lambda noun: lambda: noun() },
            { 
                "syn": "quantifier -> 'every'", 
                "sem": lambda: lambda result, range: result == range 
            },
            { 
                "syn": "quantifier -> number", 
                "sem": lambda number: lambda result, range: result == number() 
            },
            { "syn": "number -> 'two'", "sem": lambda: lambda: 2 },
            { "syn": "number -> 'three'", "sem": lambda: lambda: 3 },
            { "syn": "noun -> 'parent'", "sem": lambda: lambda: model.get_entity_range('parent') },
            { "syn": "child -> 'children'", "sem": lambda: lambda: model.get_entity_range('child') },
            { "syn": "aux -> 'has'", "sem": lambda: lambda: None },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)
        executor = SemanticExecutor(composer)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
            FindOne(executor)
        ])

        request = SentenceRequest("Every parent has two children")
        pipeline.enter(request)
        results = executor.get_results(request)
        self.assertEqual(len(results), 3)

        request = SentenceRequest("Every parent has three children")
        pipeline.enter(request)
        results = executor.get_results(request)
        self.assertEqual(len(results), 0)
