import pathlib
import unittest

from richard.core.BasicGenerator import BasicGenerator
from richard.core.Model import Model
from richard.core.Solver import Solver
from richard.core.constants import E1, E2, e1, e2
from richard.module.InferenceModule import InferenceModule
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from tests.unit.generator.TestSentenceContext import TestSentenceContext

class TestGenerator(unittest.TestCase):

    def test_generator(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/generator/resources/"

        sentence_context = TestSentenceContext()

        inferences = InferenceModule()
        inferences.import_rules(path + "inferences.pl")

        model = Model([
            inferences,
            sentence_context
        ])

        raw_grammar = [
            {
                "syn": "s(E1) -> 'OK'",
                "if": [('output_type', 'ok')]
            },
            {
                "syn": "s(E1) -> 'The above sentence is impossible'",
                "if": [('output_type', 'impossible')]
            },
            {
                "syn": "s(E1) -> np(E2) vp(E1)",
                "if": [('output_type', 'declarative'), ('output_subject', E1, E2)]
            },
            {
                "syn": "s(E1) -> named_number(E1)",
                "if": [('output_type', 'number'), ('output_number', E1)]
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

        write_grammar = SimpleGrammarRulesParser().parse(raw_grammar, write_rules=True)
        solver = Solver(model)
        generator = BasicGenerator(write_grammar, solver)

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
                'atoms': [('output_type', 'number'), ('output_number', 2)],
                "output": "two"
            },
        ]


        for test in tests:
            sentence_context.clear()
            for atom in test['atoms']:
                solver.write_atom(atom)
            output = generator.generate_output()
            self.assertEqual(output, test['output'])

