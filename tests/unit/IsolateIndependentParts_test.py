import unittest

from richard.core.constants import E1, E2, E3, E4
from richard.processor.semantic_composer.optimizer.IsolateIndependentParts import IsolateIndependentParts


class TestIsolateIndependentParts(unittest.TestCase):

    def test_simple_inference_rule_parser(self):

        tests = [
            # simplest case: E2 depends only on E1 and no other variable depends on E2
            [
                [('a', E1), ('b', E1, E2)],
                [],
                [('a', E1), ('scoped', [('b', E1, E2)])]
            ],
            # typical case: two isolated parts
            [
                [('a', E1), ('b', E1, E2), ('c', E2), ('d', E1, E3), ('e', E3)],
                [],
                [('a', E1), ('scoped', [('b', E1, E2), ('scoped', [('c', E2)])]), ('scoped', [('d', E1, E3), ('scoped', [('e', E3)])])]
            ],
            # root variable: E2 depends only on E1 but E2 is used in the result
            [
                [('a', E1), ('b', E1, E2)],
                ['E2'],
                [('a', E1), ('b', E1, E2)]
            ],
            # complex dependencies: has_population depends on city, but can't be isolated because > uses it
            [
                [('contains', E4, E1), ('city', E1), ('has_population', E1, E2), ('=', E3, 1000000), ('>', E2, E3)],
                [],
                [('contains', E4, E1), ('scoped', [('city', E1)]), ('scoped', [('has_population', E1, E2), ('scoped', [('=', E3, 1000000), ('scoped', [('>', E2, E3)])])])]
            ],
            # regression test
            [
                [('resolve_name', 'magnesium', E1), ('resolve_name', 'metal', E2), ('isa', E1, E2, E3), ('not_3v', E3, E4)],
                ['E4'],
                [('resolve_name', 'magnesium', E1), ('resolve_name', 'metal', E2), ('isa', E1, E2, E3), ('not_3v', E3, E4)],
            ],
            # regression test
            [
                [ ('resolve_name', 'Equator', E2), ('resolve_name', 'Australasia', E3), ('not', [('in', E1, E3)]) ],
                [],
                [ ('resolve_name', 'Equator', E2), ('scoped', [('resolve_name', 'Australasia', E3), ('scoped', [('not', [('in', E1, E3)])])]) ],
            ],
        ]

        for test in tests:
            atoms, root_variables, answer = test
            result = IsolateIndependentParts().isolate(atoms, root_variables)
            self.assertEqual(answer, result)
