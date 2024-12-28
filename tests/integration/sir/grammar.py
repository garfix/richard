from richard.core.constants import E1, E2, E3, E4, E5, POS_TYPE_RELATION, POS_TYPE_WORD_FORM, e1, e2, e3, Body, Range
from richard.entity.Variable import Variable
from richard.processor.parser.helper.grammar_functions import apply


T1 = Variable('T1')
T2 = Variable('T2')
T3 = Variable('T3')


def get_grammar():
    return [
        # sentence
        {
            "syn": "s() -> statement()",
            "sem": lambda statement: statement,
            "inf": [("format", "canned"), ("format_canned", "I understand")],
        },

        # statements

        # every X is a Y, where X and Y not part of the grammar
        # this is uncommon, is defines a new concept in terms of an another unknown concept
        {
            "syn": "statement() -> 'every' common_noun_name(E1) 'is' a() common_noun_name(E1)",
            "sem": lambda common_noun_name1, a, common_noun_name2: [('store', [('isa', common_noun_name1, common_noun_name2)])],
        },
        # any X is an example of a Y
        {
            "syn": "statement() -> 'any' common_noun_name(E1) 'is' 'an' 'example' 'of' a() common_noun_name(E1)",
            "sem": lambda common_noun_name1, a, common_noun_name2: [('store', [('isa', common_noun_name1, common_noun_name2)])],
        },
        # A finger is a part of a hand
        # a statement about classes as entities
        {
            "syn": "statement() -> a() common_noun_name(E1) 'is' 'a' 'part' 'of' a() common_noun_name(E1)",
            "sem": lambda a1, common_noun_name1, a2, common_noun_name2: [('store', [('part_of', common_noun_name1, common_noun_name2)])],
        },
        # There are two hands on each person
        # a statement about classes as quantified entities
        {
            "syn": "statement() -> 'there' 'are' number(E1) common_noun_name(E2) 'on' 'each' common_noun_name(E3)",
            "sem": lambda number, common_noun_name1, common_noun_name2: [('store', [('part_of', common_noun_name1, common_noun_name2), ('part_of_n', common_noun_name1, common_noun_name2, number)])],
        },
        # John is a boy
        {
            "syn": "statement() -> proper_noun(E1) 'is' a() common_noun_name(E2)",
            "sem": lambda proper_noun, a2, common_noun_name: proper_noun + [('store', [('isa', E1, common_noun_name)])],
        },
        # Every hand has 5 fingers
        {
            "syn": "statement() -> 'every' common_noun_name(E2) 'has' number(E1) common_noun_name(E3)",
            "sem": lambda common_noun_name1, number, common_noun_name2: [('store', [('part_of', common_noun_name2, common_noun_name1), ('part_of_n', common_noun_name2, common_noun_name1, number)])],
        },

        # questions

        # How many fingers does John have?
        # we don't know John, but all that matters is that it's a boy
        # determine 'how many' not by counting but by calculating
        {
            "syn": "s(E3) -> 'how' 'many' common_noun(E1) 'does' proper_noun(E2) 'have'+'?'",
            "sem": lambda common_noun1, common_noun2: common_noun1 + common_noun2 + [('count', E3, [('have', E2, E1)])],
            "inf": [("format", "number"), ("format_number", e3, ''), ('format_canned', 'The answer is {}')],
        },
        # Is a X a Y?
        {
            "syn": "s() -> 'is' a() common_noun_name(E1) a() common_noun_name(E2)~'?'",
            "sem": lambda a1, common_noun_name1, a2, common_noun_name2: [('two_way_instance_of', common_noun_name1, common_noun_name2, E3)],
            "inf": [("format", "switch"), ("format_switch", e3, 'Insufficient information'),
                    ("format_switch_value", 'sometimes', 'Sometimes'),
                    ("format_switch_value", 'yes', 'Yes')
                ],
        },

        # number
        { "syn": "number(E1) -> 'two'", "sem": lambda: 2 },
        { "syn": "number(E1) -> '5'", "sem": lambda: 5 },

        # article
        { "syn": "a() -> 'a'", "sem": lambda: [] },
        { "syn": "a() -> 'an'", "sem": lambda: [] },

        # common noun
        {
            "syn": "common_noun(E1) -> common_noun_name(E1)",
            "sem": lambda common_noun_name: [(common_noun_name, E1)], "inf": lambda common_noun_name: [('isa', e1, common_noun_name)]
        },

        # proper noun
        { "syn": "proper_noun(E1) -> /\w+/", "sem": lambda token: [('resolve_name', token, E1)] },

        # introduction of a new common noun
        { "syn": "common_noun_name(E1) -> /\w+(-\w+)*/", "sem": lambda token: token },
        { "syn": "common_noun_name(E1) -> common_noun_name(E1)+'s'", "sem": lambda common_noun_name: common_noun_name, 'boost': 1 },
    ]
