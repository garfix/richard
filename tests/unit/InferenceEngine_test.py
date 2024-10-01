import pathlib
import unittest

from richard.core.Model import Model
from richard.core.constants import E1, E2
from richard.core.Solver import Solver
from richard.entity.Variable import Variable
from richard.module.InferenceModule import InferenceModule
from richard.module.helper.SimpleInferenceRuleParser import SimpleInferenceRuleParser
from richard.type.InferenceRule import InferenceRule


class TestInferenceEngine(unittest.TestCase):

    def test_simple_inference_rule_parser(self):
        parser = SimpleInferenceRuleParser()

        tests = [
            ["river('amazon').", InferenceRule(('river', 'amazon'), [])],
            ["river('amazon').", InferenceRule(('river', 'amazon'), [])],
            ["mountain('Dante\\'s peak').", InferenceRule(('mountain', "Dante's peak"), [])],
            ['person("Robert \\"Bobby\\" Brown").', InferenceRule(('person', 'Robert "Bobby" Brown'), [])],
            ['river().', InferenceRule(('river',), [])],
            ["population('france', 43).", InferenceRule(('population', 'france', 43), [])],
            ["constant('pi', 3.14159265359).", InferenceRule(('constant', 'pi', 3.14159265359), [])],
            [
                "father(E1, E2) :- parent(E1, E2), father(E1).",
                InferenceRule(('father', Variable('E1'), Variable('E2')), [
                    ('parent', Variable('E1'), Variable('E2')),
                    ('father', Variable('E1'))
                ])
            ],
            [
                "childless(E1) :- not(parent(E1, E2)).",
                InferenceRule(('childless', Variable('E1')), [
                    ('not', [('parent', Variable('E1'), Variable('E2'))])
                ])
            ],
        ]

        for test in tests:
            question, answer = test
            result, _ = parser.parse(question)
            self.assertEqual(answer, result)


    def test_inference_engine(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/inference/"

        inferences = InferenceModule()
        inferences.import_rules(path + "rules.pl")

        model = Model([inferences])
        solver = Solver(model)

        tests = [
            [[('river', E1)], {}, [{'E1': 'amazon'}, {'E1': 'brahma_putra'}]],
            [[('river', E1)], {'E1': 'brahma_putra', 'E2': 'keep'}, [{'E1': 'brahma_putra', 'E2': 'keep'}]],
            [[('river', 'amazon')], {}, [{}]],

            [[('grand_parent', E1, E2)], {}, [{'E1': 'robert', 'E2': 'william'}, {'E1': 'martha', 'E2': 'beatrice'}, {'E1': 'martha', 'E2': 'antonio'}]],
            [[('grand_parent', E1, E2)], {'E1': 'robert', 'E2': 'william'}, [{'E1': 'robert', 'E2': 'william'}]],
            [[('grand_parent', E1, E2)], {'E1': 'martha'}, [{'E1': 'martha', 'E2': 'beatrice'}, {'E1': 'martha', 'E2': 'antonio'}]],
            [[('grand_parent', E1, 'antonio')], {}, [{'E1': 'martha'}]],
            [[('grand_parent', 'martha', 'antonio')], {'E1': 'keep'}, [{'E1': 'keep'}]],
            [[('grand_parent', 'martha', 'edward')], {}, []],
            # bindings are passed
            [[('knows', [('parent', E1, E2)], "true")], {'E1': 'martha'}, [{'E1': 'martha'}]],
            [[('knows', [('parent', E1, E2)], "true")], {'E1': 'magdalena'}, []],
        ]

        for test in tests:
            question, binding, answer = test
            result = solver.solve(question, binding)
            self.assertEqual(answer, result)
