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
        { "syn": "vp(E1, T1) -> np(E1, T2) is(E3) a(E4) np(E1, T1)", "sem": lambda np1, is1, a, np2: np1 + np2 },
        { "syn": "vp(E1, T3) -> np(E1, T2) is(E3) 'not' a(E4) np(E1, T1)", "sem": lambda np1, is1, a, np2: np1 + np2 + [('not_3v', T1, T3)] },
        { "syn": "vp(E1, T3) -> vp(E1, T1) rel_clause(E1, T2)", "sem": lambda vp, rel_clause: vp + rel_clause + [('and_3v', T1, T2, T3)] },
        { "syn": "vp(E1, T1) -> np(E1, T1) is(E3) np(E2, T1)", "sem": lambda np1, is1, np2: [('=', T1, 'true')] + np1 + np2 + [('==', E1, E2)] },
        { "syn": "vp(E1, T3) -> 'some' np(E1, T1) are(E3) np(E1, T2)", "sem": lambda np1, are, np2: np1 + np2 + [('and_3v', T1, T2, T3)] },
        # no oxide is white
        # if E1 is an oxide and E1 is white, then 'false', else 'unknown'
        { "syn": "vp(E1, T3) -> 'no' np(E1, T1) is(E3) np(E1, T2)", "sem": lambda np1, is1, np2: [('=', T1, 'true')] + [('=', T2, 'true')] + np1 + np2 + [('not_3v', T2, T3)] },
        # oxides are not white
        { "syn": "vp(E1, T3) -> np(E1, T1) are(E3) 'not' np(E1, T2)", "sem": lambda np1, are, np2: [('=', T1, 'true')] + [('=', T2, 'true')] + np1 + np2 + [('not_3v', T2, T3)] },

        # article
        { "syn": "a(E1) -> 'a'", "sem": lambda: [] },
        { "syn": "a(E1) -> 'an'", "sem": lambda: [] },

        # rel_clause
        { "syn": "rel_clause(E1, T1) -> 'that' verb(E1, T1)", "sem": lambda verb: verb },

        # verb
        { "syn": "verb(E1, T1) -> 'burns' 'rapidly'", "sem": lambda: [('burns_rapidly', E1, T1)] },

        # copula
        { "syn": "is(E1) -> 'is'", "sem": lambda: [] },
        { "syn": "are(E1) -> 'are'", "sem": lambda: [] },

        # np
        { "syn": "np(E1, T1) -> noun(E1, T1)", "sem": lambda noun: noun },
        { "syn": "np(E1, T1) -> adj(E1, T1) np(E1, T1)", "sem": lambda adj, noun: adj + noun },

        { "syn": "np(E1, T1) -> proper_noun(E1, T1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },

        # noun
        { "syn": "noun(E1, T1) -> 'metal'", "sem": lambda: [('metal', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'nonmetal'", "sem": lambda: [('nonmetal', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'white'", "sem": lambda: [('white', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'oxide'", "sem": lambda: [('oxide', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'oxides'", "sem": lambda: [('oxide', E1, T1)] },

        # proper noun
        { "syn": "proper_noun(E1, T1) -> token(E1)", "sem": lambda token: token },
        { "syn": "proper_noun(E1, T1) -> token(E1) token(E1)", "sem": lambda token1, token2: token1 + " " + token2 },
    ]
