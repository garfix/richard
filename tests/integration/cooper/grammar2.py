from richard.core.constants import E1, E2, E3, E4, E5, e1, e2, e3, Body, Range
from richard.processor.parser.helper.grammar_functions import apply
from richard.type.SemanticTemplate import SemanticTemplate



def get_grammar2():
    return [

        # sentence
        {
            "syn": "s(E1) -> vp(E1)",
            "sem": lambda vp: vp,
            "inf": [("format", "y/n/u"), ("format_ynu", e1)],
        },

        # vp
        { "syn": "vp(E1) -> np(E2) is(E3) np(E4)", "sem": lambda np1, is1, np2: np1 + np2 + [('isa', E2, E4, E1)] },
        { "syn": "vp(E1) -> np(E2) is(E3) 'not' np(E4)", "sem": lambda np1, is1, np2: np1 + np2 + [('isa', E2, E4, E5), ('not_3v', E5, E1)] },

        # copula
        { "syn": "is(E1) -> 'is'", "sem": lambda: [] },

        # np
        { "syn": "np(E1) -> 'a' proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },
        { "syn": "np(E1) -> proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },

        # proper noun
        { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },
    ]
