import unittest

from richard.core.constants import E1, E2
from richard.core.functions.matcher import match_atom, match_induction_rule
from richard.entity.Variable import Variable

A = Variable('A')
B = Variable('B')
C = Variable('C')

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


    def test_match_atom(self):

        tests = [
            {
                'atom1': ('name', A, B),
                'atom2': ('name', '$1', '$2'),
                'binding': {},
                'result': {'A': '$1', 'B': '$2'}
            },
            {
                'atom1': ('name', A, A),
                'atom2': ('name', '$1', '$2'),
                'binding': {},
                'result': None
            },
            {
                'atom1': ('name', [(A, B)], [(B, C)]),
                'atom2': ('name', [('$1', '$2')], [('$2', '$3')]),
                'binding': {},
                'result': {'A': '$1', 'B': '$2', 'C': '$3'}
            },
            {
                'atom1': ('name', [(A, B)], [(B, C)]),
                'atom2': ('name', [('$1', '$2')], [('$3', '$2')]),
                'binding': {},
                'result': None
            },
            {
                'atom1': ('name', [('$4', '$5')], [(B, C)]),
                'atom2': ('name', None, [('$2', '$3')]),
                'binding': {},
                'result': {'B': '$2', 'C': '$3'}
            },
        ]

        for test in tests:
            result = match_atom(test['atom1'], test['atom2'], test['binding'])
            self.assertEqual(result, test['result'])


