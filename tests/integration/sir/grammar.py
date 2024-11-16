from richard.core.constants import E1, E2, E3, E4, E5, POS_TYPE_RELATION, POS_TYPE_WORD_FORM, e1, e2, e3, Body, Range
from richard.entity.GrammarRule import GrammarRule
from richard.entity.RuleConstituent import RuleConstituent
from richard.entity.Variable import Variable
from richard.processor.parser.helper.grammar_functions import apply


T1 = Variable('T1')
T2 = Variable('T2')
T3 = Variable('T3')


def get_grammar():
    return [
        # sentence

        # every X is a Y, where X and Y not part of the grammar
        # this is uncommon, is defines a new concept in terms of an another unknown concept
        {
            "syn": "s() -> 'every' common_noun(E1) 'is' a() common_noun(E1)",
            "sem": lambda common_noun1, a2, common_noun2: [('learn_rule', common_noun2[0], common_noun1)],
            "inf": [("format", "canned"), ("format_canned", "I understand")],
        },

        # article
        { "syn": "a() -> 'a'", "sem": lambda: [] },
        { "syn": "a() -> 'an'", "sem": lambda: [] },

        # noun
        { "syn": "noun(E1) -> common_noun(E1)", "sem": lambda common_noun: common_noun },
        { "syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: proper_noun },

        # common noun
        { "syn": "common_noun(E1) -> 'person'", "sem": lambda: [('person', E1)] },

        # proper noun
        { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: [('resolve_name', token, E1)] },

        # introduction of a new common noun
        { "syn": "common_noun_name(E1) -> token(E1)", "sem": lambda token: token },

        # introduction of a new common noun
        { "syn": "common_noun(E1) -> token(E1)", "sem": lambda token: [ (token, E1) ],
          "exec": lambda token: [
            ('learn_grammar_rule', { "syn": f"common_noun(E1) -> '{token}'", "sem": lambda: [(token, E1)] }),
            ('add_relation', token, ['id']),
        ] },
    ]
