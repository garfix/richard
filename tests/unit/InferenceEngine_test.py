import pathlib
import unittest

from richard.core.Model import Model
from richard.core.constants import E1, E2
from richard.core.Solver import Solver
from richard.entity.Variable import Variable
from richard.module.InferenceModule import InferenceModule
from richard.module.helper.SimpleInferenceRuleParser import SimpleInferenceRuleParser
from richard.entity.InferenceRule import InferenceRule


class TestInferenceEngine(unittest.TestCase):

    def test_simple_inference_rule_parser(self):
        parser = SimpleInferenceRuleParser()

        tests = [
            ["river('amazon').", [InferenceRule(('river', 'amazon'), [])]],
            # with comment
            ["river('amazon')\n\t#remark\n.", [InferenceRule(('river', 'amazon'), [])]],
            ["mountain('Dante\\'s peak').", [InferenceRule(('mountain', "Dante's peak"), [])]],
            ['person("Robert \\"Bobby\\" Brown").', [InferenceRule(('person', 'Robert "Bobby" Brown'), [])]],
            ['river().', [InferenceRule(('river',), [])]],
            ["population('france', 43).", [InferenceRule(('population', 'france', 43), [])]],
            ["constant('pi', 3.14159265359).", [InferenceRule(('constant', 'pi', 3.14159265359), [])]],
            [
                "father(E1, E2) :- parent(E1, E2), father(E1).",
                [InferenceRule(('father', Variable('E1'), Variable('E2')), [
                    ('parent', Variable('E1'), Variable('E2')),
                    ('father', Variable('E1'))
                ])]
            ],
            [
                "childless(E1) :- not(parent(E1, E2)).",
                [InferenceRule(('childless', Variable('E1')), [
                    ('not', [('parent', Variable('E1'), Variable('E2'))])
                ])]
            ],
            # grouped atoms with parenthesis
            [
                "switch(E1) :- or((a(1), b(2)), (c(3), d(4))).",
                [InferenceRule(('switch', Variable('E1')), [
                    ('or',
                        [('a', 1), ('b', 2)],
                        [('c', 3), ('d', 4)],
                    )
                ])]
            ],
            # unification
            ["pred(X) :- X = 2.", [InferenceRule(('pred', Variable('X')), [('$unification', Variable('X'), 2)])]],
            ["pred(X) :- X = pred2(A).", [InferenceRule(('pred', Variable('X')), [('$unification', Variable('X'), [('pred2', Variable('A'))])])]],
            ["pred(X) :- pred2(A) = X.", [InferenceRule(('pred', Variable('X')), [('$unification', [('pred2', Variable('A'))], Variable('X'))])]],
        ]

        for test in tests:
            question, answer = test
            rules, _ = parser.parse_rules(question)
            self.assertEqual(answer, rules)


    def test_inference_engine(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/inference/"

        inferences = InferenceModule()
        inferences.import_rules(path + "rules.pl")

        model = Model([inferences])
        solver = Solver(model)

        tests = [
            [[('river', 'brahma_putra')], [{}]],
            [[('river', 'amazon')], [{}]],

            [[('grand_parent', E1, E2)], [{'E1': 'robert', 'E2': 'william'}, {'E1': 'martha', 'E2': 'beatrice'}, {'E1': 'martha', 'E2': 'antonio'}]],
            [[('grand_parent', 'robert', 'william')], [{}]],
            [[('grand_parent', 'martha', E2)], [{'E2': 'beatrice'}, {'E2': 'antonio'}]],
            [[('grand_parent', E1, 'antonio')], [{'E1': 'martha'}]],
            [[('grand_parent', 'martha', 'antonio')], [{}]],
            [[('grand_parent', 'martha', 'edward')], []],
            # bindings are passed
            [[('knows', [('parent', 'martha', E2)], "true")], [{}]],
            [[('knows', [('parent', 'magdalena', E2)], "true")], []],
            [[('ancestor', 'robert', 'antonio')], [{}]],
            [[('related', 'robert', 'antonio')], [{}]],
            [[('related', 'robert', 'robert')], [{}]],
            [[('related', 'robert', 'xantippe')], []],
            [[('related', E1, E1)], [{'E1': 'jennifer'}]],
            [[('related', 'jennifer', 'jennifer')], [{}]],
            [[('related', 'robert', 'robert')], [{}]],
            # test disjunction
            [[('family', E1, 'martha')], [{'E1': 'robert'}]],
            [[('family', E1, 'william')], [{'E1': 'robert'}]],
            [[('sibling', 'spike', E1)], [{'E1': 'suzy'}]],
            [[('country', E1)], [{'E1': 'netherlands'}]],
        ]

        for test in tests:
            question, answer = test
            result = solver.solve(question)
            self.assertEqual(answer, result)
