import unittest

from richard.block.TryFirst import TryFirst
from richard.core.BasicGenerator import BasicGenerator
from richard.core.Model import Model
from richard.core.System import System
from richard.block.FindOne import FindOne
from richard.core.constants import E1, e1
from richard.entity.SentenceRequest import SentenceRequest
from richard.module.BasicOutputBuffer import BasicOutputBuffer
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from tests.unit.atom_executor.write_grammar import get_write_grammar
from tests.unit.atom_executor.TestDialogContext import TestDialogContext
from tests.unit.atom_executor.TestModule import TestModule

class TestAtomExecutor(unittest.TestCase):

    def test_produce_exception_output(self):
        """
        resolve_name fails to find "John" and produces output
        It's error is passed to the ProcessingResult and the BlockResult
        and ends up in the response
        """

        read_grammar = [
            { "syn": "s(E1) -> noun(E1) verb(V)", "sem": lambda noun, verb: noun + verb },
            { "syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },
            { "syn": "proper_noun(E1) -> /\w+/", "sem": lambda token: token },
            { "syn": "verb(E1) -> 'walks'", "sem": lambda: [('walks', E1)] },
        ]

        facts = TestModule()
        output_buffer = BasicOutputBuffer()

        model = Model([
            facts,
            output_buffer,
        ])

        read_grammar = SimpleGrammarRulesParser().parse_read_grammar(read_grammar)
        write_grammar = SimpleGrammarRulesParser().parse_write_grammar(get_write_grammar())
        parser = BasicParser(read_grammar)
        composer = SemanticComposer(parser)
        executor = AtomExecutor(composer, model)
        generator = BasicGenerator(write_grammar, model, output_buffer)

        pipeline = System(
            model=model,
            input_pipeline=[
                FindOne(parser),
                TryFirst(composer),
                TryFirst(executor),
            ],
            output_generator=generator)

        pipeline.enter(SentenceRequest("John walks"))
        output = generator.generate_output()

        self.assertEqual("Name not found: john", output)


    def test_inferences(self):
        """
        Contains an inference that stores an atom in a data store
        Contains executable code that stores an atom in a data store
        """

        simple_grammar = [
            {
                "syn": "s(E1) -> noun(E1) 'be'",
                "sem": lambda noun: noun
            },
            {
                "syn": "s(E1) -> /\w+/ 'exist'",
                "sem": lambda token: [],
                "exec": lambda token: [('store', [('concept', token.lower())])]
            },
            {
                "syn": "noun(E1) -> 'continents'",
                "sem": lambda: [('continent', E1)],
                "dialog": [('isa', e1, 'continent')]
            },
        ]

        facts = TestModule()
        dialog_context = TestDialogContext()

        model = Model([
            facts,
            dialog_context
        ])

        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)
        executor = AtomExecutor(composer, model)

        system = System(
            model=model,
            input_pipeline=[
                FindOne(parser),
                TryFirst(composer),
                TryFirst(executor),
            ]
        )

        # test the inference
        system.enter(SentenceRequest("Continents be"))
        results = dialog_context.data_source.select("isa", ['entity', 'type'], [None, None])
        self.assertEqual(["$1", "continent"], results[0])

        # test the executable code
        system.enter(SentenceRequest("Continents exist"))
        results = dialog_context.data_source.select("concept", ['type'], [None])
        self.assertEqual(["continents"], results[0])

