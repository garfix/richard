import unittest

from richard.block.TryFirst import TryFirst
from richard.core.Model import Model
from richard.core.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.core.constants import E1
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from tests.unit.atom_executor.TesModule import TestModule

class TestAtomExecutor(unittest.TestCase):

    def test_processing_exception(self):
        """
        resolve_name fails to find "John" and throws a ProcessingException
        It's error is passed to the ProcessingResult and the BlockResult
        and ends up in the response
        """

        grammar = [
            { "syn": "s(E1) -> noun(E1) verb(V)", "sem": lambda noun, verb: noun + verb },
            { "syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },
            { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },
            { "syn": "verb(E1) -> 'walks'", "sem": lambda: [('walks', E1)] },
        ]

        facts = TestModule()

        model = Model([
            facts,
        ])

        tokenizer = BasicTokenizer()
        parser = BasicParser(grammar, tokenizer)
        composer = SemanticComposer(parser)
        executor = AtomExecutor(composer, model)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            TryFirst(composer),
            TryFirst(executor),
        ])

        output = pipeline.enter(SentenceRequest("John walks"))

        self.assertEqual("Name not found: john", output)
