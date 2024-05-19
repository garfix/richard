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
from richard.semantics.commands import exists, find
from richard.store.MemoryDb import MemoryDb


class TestChat80(unittest.TestCase):
    """
    Mimics a Chat80 dialog (found here: https://github.com/JanWielemaker/chat80/blob/master/prolog/chat80/demo)
    Topics:
    - aggregation
    - extraposition (long distance despendencies)
    - relative clauses
    """
   
    def test_chat80(self):

        # database

        db = MemoryDb()
        db.insert(Record('river', {'id': 'amazon'}))
        db.insert(Record('river', {'id': 'brahmaputra'}))
        
        db.insert(Record('country', {'id': 'afghanistan'}))
        db.insert(Record('country', {'id': 'china'}))

        db.insert(Record('borders', {'county_id1': 'afghanistan', 'country_id2': 'china'}))

        # domain

        domain = Domain([
            Entity("river", lambda: db.select(Record('river')).field('id')),
            Entity("country", lambda: db.select(Record('country')).field('id')),
        ], [
            Relation("in_continent", ['place', 'continent'], lambda parent, child: db.select(Record('has_child', {'parent': parent, 'child': child}))),
            Relation("borders", ['country', 'country'], lambda country1, country2: db.select(Record('borders', {'county_id1': country1, 'county_id1': country2}))),
        ])

        # grammar

        grammar = [
            { 
                "syn": "s -> 'what' nbar 'are' 'there' '?'", 
                "sem": lambda nbar: lambda: nbar()
            },
            { 
                "syn": "s -> 'does' np vp_no_sub '?'", 
                "sem": lambda np, vp_no_sub: lambda: find(np(), vp_no_sub)
            },
            { 
                "syn": "vp_no_sub -> tv np", 
                "sem": lambda verb, np: lambda subject: find(np(), verb(subject))
            },
            { "syn": "np -> nbar", "sem": lambda nbar: lambda: (exists, nbar) },
            { "syn": "nbar -> noun", "sem": lambda noun: lambda: noun() },
            { "syn": "noun -> proper_noun", "sem": lambda proper_noun: lambda: proper_noun() },

            { "syn": "noun -> 'rivers'", "sem": lambda: lambda: domain.get_entity_ids('river') },
            { "syn": "tv -> 'border'", "sem": lambda: 
                lambda object: 
                    lambda subject: 
                        domain.relation_exists('borders', [subject, object]) },

            # todo
            { "syn": "proper_noun -> 'afghanistan'", "sem": lambda: lambda: ['afghanistan'] },
            { "syn": "proper_noun -> 'china'", "sem": lambda: lambda: ['china'] },
        ]

        # pipeline

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

        # testing

        tests = [
            ["What rivers are there?", ['amazon', 'brahmaputra']],
            ["Does Afghanistan border China?", ['afghanistan']]
        ]

        for test in tests:
            question, answer = test
            request = SentenceRequest(question)
            result = pipeline.enter(request)

            if not result.error_code == "":
                print(result.error_code, result.error_args) 
                break

            results = executor.get_results(request)
            self.assertEqual(set(answer), set(results))
