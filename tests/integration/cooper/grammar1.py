from richard.core.constants import E1, E2, E3, E4, e1, e2, e3, Body, Range
from richard.processor.parser.helper.grammar_functions import apply


def get_grammar1():
    return [
        # sentence
        {
            "syn": "s(E1) -> noun(E1) is(E3) a(E4) noun(E2)",
            "sem": lambda noun1, is1, a, noun2: noun1 + noun2 + [('store', ('isa', e1, e2))],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        {
            "syn": "s(E1) -> noun(E1) is(E3) 'not' a(E4) noun(E2)",
            "sem": lambda noun1, is1, a, noun2: noun1 + noun2 + [('store', ('not_isa', e1, e2))],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },

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
