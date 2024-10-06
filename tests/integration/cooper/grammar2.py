from richard.core.constants import E1, E2, E3, E4, E5, e1, e2, e3, Body, Range
from richard.entity.ReifiedVariable import ReifiedVariable
from richard.entity.Variable import Variable
from richard.processor.parser.helper.grammar_functions import apply

T1 = Variable('T1')
T2 = Variable('T2')
T3 = Variable('T3')

t1 = ReifiedVariable('T1')

# This grammar uses variables not only to link regular entities, but truth values as well
def get_grammar2():
    return [

        # sentence
        {
            "syn": "s(T1) -> vp(E1, T1)",
            "sem": lambda vp: vp,
            "inf": [("format", "y/n/u"), ("format_ynu", t1)],
        },

        # vp
        { "syn": "vp(E1, T1) -> np(E1) is(E3) np(E2)", "sem": lambda np1, is1, np2: np1 + np2 + [('isa', E1, E2, T1)] },
        { "syn": "vp(E1, T2) -> np(E1) is(E3) 'not' np(E2)", "sem": lambda np1, is1, np2: np1 + np2 + [('isa', E1, E2, T1), ('not_3v', T1, T2)] },
        { "syn": "vp(E1, T3) -> vp(E1, T1) rel_clause(E1, T2)", "sem": lambda vp, rel_clause: vp + rel_clause + [('and_3v', T1, T2, T3)] },

        # rel_clause
        { "syn": "rel_clause(E1, T1) -> 'that' verb(E1, T1)", "sem": lambda verb: verb },

        # verb
        { "syn": "verb(E1, T1) -> 'burns' 'rapidly'", "sem": lambda: [('burns_rapidly', E1, T1)] },

        # copula
        { "syn": "is(E1) -> 'is'", "sem": lambda: [] },

        # np
        { "syn": "np(E1) -> 'a' proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },
        { "syn": "np(E1) -> proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },

        # proper noun
        { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },
    ]
