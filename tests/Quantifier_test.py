import unittest

from richard.Domain import Domain
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
from richard.semantics.commands import find
from richard.store.MemoryDb import MemoryDb


class TestQuantifier(unittest.TestCase):
   
    def test_quantifier(self):

        db = MemoryDb()
        db.insert(Record('has_child', {'parent': 'mary', 'child': 'lucy'}))
        db.insert(Record('has_child', {'parent': 'mary', 'child': 'bonny'}))
        db.insert(Record('has_child', {'parent': 'barbara', 'child': 'john'}))
        db.insert(Record('has_child', {'parent': 'barbara', 'child': 'chuck'}))
        db.insert(Record('has_child', {'parent': 'william', 'child': 'oswald'}))
        db.insert(Record('has_child', {'parent': 'william', 'child': 'bertrand'}))

        domain = Domain([
            Entity("parent", lambda: db.select(Record('has_child')).field('parent')),
            Entity("child", lambda: db.select(Record('has_child')).field('child')),
        ], [
            Relation("has_child", ['parent', 'child'], lambda parent, child: db.select(Record('has_child', {'parent': parent, 'child': child}))),
        ])

        grammar = [
            { 
                "syn": "s -> np vp_no_sub", 
                "sem": lambda np, vp_no_sub: lambda: find(np(), vp_no_sub) 
            },
            { 
                "syn": "vp_no_sub -> aux qp child", 
                "sem": lambda aux, qp, child:
                        lambda subject: find(
                            (qp, child),
                            lambda object: domain.relation_exists('has_child', [subject, object]))
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
            { "syn": "noun -> 'parent'", "sem": lambda: lambda: domain.get_entity_ids('parent') },
            { "syn": "child -> 'children'", "sem": lambda: lambda: domain.get_entity_ids('child') },
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
