import unittest

from richard.core.constants import E1, E2
from richard.entity.Variable import Variable
from richard.entity.InductionRule import InductionRule
from richard.module.helper.SimpleInferenceRuleParser import SimpleInferenceRuleParser


class TestInductionModule(unittest.TestCase):

    def test_simple_inference_rule_parser(self):
        parser = SimpleInferenceRuleParser()

        tests = [
            # ["orang_utan(E1) => ape(E1).", [InductionRule([('orang_utan', Variable('E1'))], [('ape', Variable('E1'))])]],
            ["female(E1), cow(E1), young(E1) => heifer(E1), bovine(E1).", [InductionRule(
                [('female', Variable('E1')), ('cow', Variable('E1')), ('young', Variable('E1'))],
                [('heifer', Variable('E1')), ('bovine', Variable('E1'))])]],
        ]

        for test in tests:
            question, answer = test
            induction_rules, _ = parser.parse_induction_rules(question)
            self.assertEqual(answer, induction_rules)
