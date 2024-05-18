import unittest

from richard.Domain import Domain
from richard.Pipeline import Pipeline
from richard.block.FirstSuccess import FirstSuccess
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


class TestChat80(unittest.TestCase):
    """
    Mimics a Chat80 dialog (found here: https://github.com/JanWielemaker/chat80/blob/master/prolog/chat80/demo)
    Topics:
    - aggregation
    - extraposition (long distance despendencies)
    - relative clauses
    """
   
    def test_chat80(self):

        db = MemoryDb()
        db.insert(Record('river', {'id': 'amazon'}))
        db.insert(Record('river', {'id': 'brahmaputra'}))

        domain = Domain([
            Entity("river", lambda: db.select(Record('river')).field('id')),
        ], [
            Relation("in_continent", ['place', 'continent'], lambda parent, child: db.select(Record('has_child', {'parent': parent, 'child': child}))),
        ])

        grammar = [
            { 
                "syn": "s -> 'what' nbar 'are' 'there' '?'", 
                "sem": lambda nbar: lambda: nbar()
            },
            { "syn": "nbar -> noun", "sem": lambda noun: lambda: noun() },
            { "syn": "noun -> 'rivers'", "sem": lambda: lambda: domain.get_entity_ids('river') },
        ]

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)
        executor = SemanticExecutor(composer)

        pipeline = Pipeline([
            FirstSuccess(tokenizer),
            FirstSuccess(parser),
            FirstSuccess(composer),
            FirstSuccess(executor)
        ])

        tests = [
            ["What rivers are there?", ['amazon', 'brahmaputra']]
        ]

        for test in tests:
            question, answer = test
            request = SentenceRequest(question)
            result = pipeline.enter(request)

            if not result.successful():
               print(result.error_code, result.error_args) 

            print(result.products)

            results = executor.get_results(request)
            self.assertEqual(list(set(answer)), results)
