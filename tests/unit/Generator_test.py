import pathlib
import unittest

from richard.core.BasicGenerator import BasicGenerator
from richard.core.Model import Model
from richard.core.Solver import Solver
from richard.core.constants import E1, E2, e1, e2
from richard.module.InferenceModule import InferenceModule
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from tests.unit.generator.TestOutputBuffer import TestOutputBuffer

class TestGenerator(unittest.TestCase):

    def test_generator(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/generator/"

        output_buffer = TestOutputBuffer()

        inferences = InferenceModule()
        inferences.import_rules(path + "inferences.pl")

        model = Model([
            inferences,
            output_buffer
        ])

        raw_grammar = [
            {
                "syn": "s() -> 'OK'",
                "if": [('output_type', 'ok')]
            },
            {
                "syn": "s() -> 'The above sentence is impossible'",
                "if": [('output_type', 'impossible')]
            },
            {
                "syn": "s() -> np(E2) vp(E1)",
                "if": [('output_type', 'declarative'), ('output_subject', E1, E2)]
            },
            {
                "syn": "s() -> named_number(E1)",
                "if": [('output_type', 'scalar'), ('output_value', E1)]
            },
            {
                "syn": "vp(E1) -> verb(E1) np(E2)",
                "if": [('output_object', E1, E2)]
            },
            {
                "syn": "np(E1) -> text(E2)",
                "if": [('resolve_name', E2, E1)]
            },
            {
                "syn": "verb(E1) -> 'married'",
                "if": [('output_predicate', E1, 'marry')]
            },
            { "syn": "named_number(E1) -> 'one'", "if": [('equals', E1, 1)] },
            { "syn": "named_number(E1) -> 'two'", "if": [('equals', E1, 2)] },
        ]

        write_grammar = SimpleGrammarRulesParser().parse_write_grammar(raw_grammar)
        generator = BasicGenerator(write_grammar, model, output_buffer)

        tests = [
            {
                'atoms': [('output_type', 'ok')],
                "output": "OK"
            },
            {
                'atoms': [('output_type', 'impossible')],
                "output": "The above sentence is impossible"
            },
            {
                'atoms': [('output_type', 'declarative'), ('output_predicate', '5', 'marry'), ('output_subject', '5', '10892'), ('output_object', '5', '37216')],
                "output": "Jane married John"
            },
            {
                'atoms': [('output_type', 'scalar'), ('output_value', 2)],
                "output": "two"
            },
        ]

        solver = Solver(model)

        for test in tests:
            output_buffer.clear()
            for atom in test['atoms']:
                solver.write_atom(atom)
            output = generator.generate_output()
            self.assertEqual(output, test['output'])

