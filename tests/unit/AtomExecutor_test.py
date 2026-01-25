import unittest

from richard.core.BasicGenerator import BasicGenerator
from richard.core.BasicSystem import BasicSystem
from richard.core.Model import Model
from richard.core.constants import E1, e1
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.Variable import Variable
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

        system = BasicSystem(
            model=model,
            parser=parser,
            composer=composer,
            executor=executor,
            output_generator=generator
        )

        system.enter(SentenceRequest("John walks"))
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

        system = BasicSystem(
            model=model,
            parser=parser,
            composer=composer,
            executor=executor
        )

        # test the inference
        system.enter(SentenceRequest("Continents be"))
        results = dialog_context.data_source.select("isa", ['entity', 'type'], [Variable("E1"), Variable("E2")])
        self.assertEqual(["$1", "continent"], results[0])

        # test the executable code
        system.enter(SentenceRequest("Continents exist"))
        results = dialog_context.data_source.select("concept", ['type'], [Variable("E1")])
        self.assertEqual(["continents"], results[0])

