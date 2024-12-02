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
        # A finger is a part of a hand
        # a statement about classes as entities
        {
            "syn": "s() -> a() common_noun_name(E1) 'is' 'a' 'part' 'of' a() common_noun_name(E1)",
            "sem": lambda a1, common_noun_name1, a2, common_noun_name2: [('store', [('part_of', common_noun_name1, common_noun_name2)])],
            "inf": [("format", "canned"), ("format_canned", "I understand")],
        },
        # There are two hands on each person
        # a statement about classes as quantified entities
        {
            "syn": "s() -> 'there' 'are' number(E1) common_noun_name(E2) 'on' 'each' common_noun_name(E3)",
            "sem": lambda number, common_noun_name1, common_noun_name2: [('store', [('part_of_n', common_noun_name1, common_noun_name2, number)])],
            "inf": [("format", "canned"), ("format_canned", "I understand")],
        },
        # How many fingers does John have?
        # we don't know John, but all that matters is that it's a boy
        # determine 'how many' not by counting but by calculating
        {
            "syn": "s(E3) -> 'how' 'many' common_noun(E1) 'does' proper_noun(E2) 'have' '?'",
            "sem": lambda common_noun1, common_noun2: common_noun1 + common_noun2 + [('count', E3, [('have', E2, E1)])],
            "inf": [("format", "number"), ("format_number", e3, '')],
        },

        # number
        { "syn": "number(E1) -> 'two'", "sem": lambda: 2 },

        # article
        { "syn": "a() -> 'a'", "sem": lambda: [] },
        { "syn": "a() -> 'an'", "sem": lambda: [] },

        # noun
        { "syn": "noun(E1) -> common_noun(E1)", "sem": lambda common_noun: common_noun },
        { "syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: proper_noun },

        # common noun
        { "syn": "common_noun(E1) -> 'person'", "sem": lambda: [('person', E1)],      "inf": [('isa', e1, 'person')] },
        { "syn": "common_noun(E1) -> 'fingers'", "sem": lambda: [('finger', E1)],     "inf": [('isa', e1, 'finger')] },

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
