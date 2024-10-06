from richard.core.constants import E1, E2, E3, E4, E5, e1, e2, e3, Body, Range
from richard.processor.parser.helper.grammar_functions import apply


def get_grammar1():
    return [
        # sentence

        # X is a Y
        {
            "syn": "s(E1) -> noun(E1) is(E3) a(E4) noun(E2)",
            "sem": lambda noun1, is1, a, noun2: noun1 + noun2 + [('store', ('isa', E1, E2, 'true'))],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # no X is a Y
        {
            "syn": "s(E1) -> 'no' noun(E1) is(E3) a(E4) noun(E2)",
            "sem": lambda noun1, is1, a, noun2: noun1 + noun2 + [('learn_rule', ('isa', E5, E2, 'false'), [('isa', E5, E1, 'true')])],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # noun verb
        {
            "syn": "s(E1) -> noun(E1) verb(E1)",
            "sem": lambda noun, verb: noun + [('store', verb)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },

        # verb
        { "syn": "verb(E1) -> 'burns' 'rapidly'", "sem": lambda: ('burns_rapidly', E1, 'true') },

        # copula
        { "syn": "is(E1) -> 'is'", "sem": lambda: [] },

        # article
        { "syn": "a(E1) -> 'a'", "sem": lambda: [] },
        { "syn": "a(E1) -> 'an'", "sem": lambda: [] },

        # noun
        { "syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },


        # proper noun
        { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },
    ]
