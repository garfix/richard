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
            "syn": "s() -> 'every' common_noun_name(E1) 'is' a() common_noun_name(E1)",
            "sem": lambda common_noun_name1, a2, common_noun_name2: [('store', [('isa', common_noun_name1, common_noun_name2)])],
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
            "sem": lambda number, common_noun_name1, common_noun_name2: [('store', [('part_of', common_noun_name1, common_noun_name2), ('part_of_n', common_noun_name1, common_noun_name2, number)])],
            "inf": [("format", "canned"), ("format_canned", "I understand")],
        },
        # How many fingers does John have?
        # we don't know John, but all that matters is that it's a boy
        # determine 'how many' not by counting but by calculating
        {
            "syn": "s(E3) -> 'how' 'many' common_noun(E1) 'does' proper_noun(E2) 'have'+'?'",
            "sem": lambda common_noun1, common_noun2: common_noun1 + common_noun2 + [('count', E3, [('have', E2, E1)])],
            "inf": [("format", "number"), ("format_number", e3, ''), ('format_canned', 'The answer is {}')],
        },
        # John is a boy
        {
            "syn": "s() -> proper_noun(E1) 'is' a() common_noun_name(E2)",
            "sem": lambda proper_noun, a2, common_noun_name: proper_noun + [('store', [('isa', E1, common_noun_name)])],
            "inf": [("format", "canned"), ("format_canned", "I understand")],
        },
        # Every hand has 5 fingers
        {
            "syn": "s() -> 'every' common_noun_name(E2) 'has' number(E1) common_noun_name(E3)",
            "sem": lambda common_noun_name1, number, common_noun_name2: [('store', [('part_of', common_noun_name2, common_noun_name1), ('part_of_n', common_noun_name2, common_noun_name1, number)])],
            "inf": [("format", "canned"), ("format_canned", "I understand")],
        },

        # number
        { "syn": "number(E1) -> 'two'", "sem": lambda: 2 },
        { "syn": "number(E1) -> '5'", "sem": lambda: 5 },

        # article
        { "syn": "a() -> 'a'", "sem": lambda: [] },
        { "syn": "a() -> 'an'", "sem": lambda: [] },

        # common noun
        { "syn": "common_noun(E1) -> /\w+/", "sem": lambda token: [(token, E1)], "inf": lambda token: [('isa', e1, token)] },
        { "syn": "common_noun(E1) -> common_noun(E1)+'s'", "sem": lambda common_noun: common_noun },

        # proper noun
        { "syn": "proper_noun(E1) -> /\w+/", "sem": lambda token: [('resolve_name', token, E1)] },

        # introduction of a new common noun
        { "syn": "common_noun_name(E1) -> /\w+/", "sem": lambda token: token },
        { "syn": "common_noun_name(E1) -> /\w+/+'s'", "sem": lambda token: token, 'boost': 1 },
    ]
