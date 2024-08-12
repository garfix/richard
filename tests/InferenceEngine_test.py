import pathlib
import unittest

from richard.Model import Model
from richard.constants import E1, E2
from richard.Solver import Solver
from richard.entity.Variable import Variable
from richard.module.InferenceModule import InferenceModule
from richard.module.helper.SimpleInferenceRuleParser import SimpleInferenceRuleParser
from richard.type.InferenceRule import InferenceRule


class TestInferenceEngine(unittest.TestCase):

    def test_simple_inference_rule_parser(self):
        parser = SimpleInferenceRuleParser()

        tests = [
            ["river('amazon').", InferenceRule(('river', 'amazon'), [])],
            [
                "father(E1, E2) :- parent(E1, E2), father(E1).", 
                InferenceRule(('father', Variable('E1'), Variable('E2')), [
                    ('parent', Variable('E1'), Variable('E2')),
                    ('father', Variable('E1'))
                ])],
        ]

        for test in tests:
            question, answer = test
            result = parser.parse(question)
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
        ]

        for test in tests:
            question, binding, answer = test
            result = solver.solve(question, binding)
            self.assertEqual(answer, result)
