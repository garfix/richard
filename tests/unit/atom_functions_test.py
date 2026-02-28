import unittest

from richard.core.constants import E1, E2
from richard.core.functions.matcher import match_induction_rule
from richard.entity.Variable import Variable

A = Variable('A')
B = Variable('B')

class TestAtomFunctions(unittest.TestCase):

    def test_match_induction_rule(self):

        sentence = [('name', E1, 'Mary'), ('name', E2, 'John'), ('play_tennis', E1, E2), ('win', E1), ('father', 'Bill', E1)]

        tests = [
            {
                'antecedent': [('name', A, B)],
                'sentence': sentence,
                'bindings': [{'A': E1, 'B': 'Mary'}, {'A': E2, 'B': 'John'}]
            },
            {
                'antecedent': [('win', A), ('name', A, B)],
                'sentence': sentence,
                'bindings': [{'A': E1, 'B': 'Mary'}]
            },
            {
                'antecedent': [('name', A, 'John'), ('win', A)],
                'sentence': sentence,
                'bindings': []
            },
            {
                'antecedent': [('name', A, A)],
                'sentence': sentence,
                'bindings': [{'A': 'Mary'}, {'A': 'John'}]
            },
            {
                'antecedent': [('father', A, A)],
                'sentence': sentence,
                'bindings': [{'A': 'Bill'}]
            },
        ]

        for test in tests:
            bindings = match_induction_rule(test['antecedent'], test['sentence'])
            self.assertEqual(bindings, test['bindings'])


