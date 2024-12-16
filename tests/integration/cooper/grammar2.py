from richard.core.constants import E1, E2, E3, E4, E5, e1, e2, e3, Body, Range
from richard.entity.ReifiedVariable import ReifiedVariable
from richard.entity.Variable import Variable
from richard.processor.parser.helper.grammar_functions import apply

T1 = Variable('T1')
T2 = Variable('T2')
T3 = Variable('T3')
T4 = Variable('T4')
T5 = Variable('T5')
T6 = Variable('T6')

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
        { "syn": "vp(E1, T3) -> np(E1, T2) is() a() np(E1, T1)", "sem": lambda np1, is1, a, np2: np1 + np2 + [('and_3v', T1, T2, T3)] },
        { "syn": "vp(E1, T3) -> np(E1, T2) is() 'not' a() np(E1, T1)", "sem": lambda np1, is1, a, np2: np1 + np2 + [('not_3v', T1, T3)] },
        { "syn": "vp(E1, T3) -> vp(E1, T1) rel_clause(E1, T2)", "sem": lambda vp, rel_clause: vp + rel_clause + [('and_3v', T1, T2, T3)] },
        { "syn": "vp(E1, T3) -> np(E1, T1) is() np(E1, T2)", "sem": lambda np1, is1, np2: np1 + np2 + [('and_3v', T1, T2, T3)] },
        { "syn": "vp(E1, T3) -> 'some' np(E1, T1) are() np(E1, T2)", "sem": lambda np1, are, np2: np1 + np2 + [('and_3v', T1, T2, T3)] },
        # no oxide is white
        # if E1 is an oxide and E1 is white, then 'false', else 'unknown'
        { "syn": "vp(E1, T3) -> 'no' np(E1, T1) is() np(E1, T2)", "sem": lambda np1, is1, np2: [('=', T1, 'true')] + [('=', T2, 'true')] + np1 + np2 + [('not_3v', T2, T3)] },
        # oxides are not white
        { "syn": "vp(E1, T3) -> np(E1, T1) are() 'not' np(E1, T2)", "sem": lambda np1, are, np2: [('=', T1, 'true')] + [('=', T2, 'true')] + np1 + np2 + [('not_3v', T2, T3)] },
        # every oxide is an oxide
        { "syn": "vp(E1, T3) -> 'every' np(E1, T1) is() a() np(E1, T2)", "sem": lambda np1, is1, a, np2: [('=', T1, 'true')] + [('=', T2, 'true')] + np1 + np2 + [('and_3v', T1, T2, T3)] },
        # ferrous sulfide is not a compound that is not dark-gray
        { "syn": "vp(E1, T6) -> np(E1, T1) is() 'not' a() np(E1, T2) 'that' is() 'not' np(E1, T3)",
          "sem": lambda np1, is1, a, np2, is2, np3: np1 + np2 + np3 + [('not_3v', T3, T4), ('and_3v', T2, T4, T5), ('not_3v', T5, T6)]},
        # ferrous sulfide is not brittle
        # anything that is not a compound is not ferrous sulfide
        { "syn": "vp(E1, T4) -> np(E1, T1) is() 'not' np(E1, T2)",
          "sem": lambda np1, is2, np2: np1 + np2 + [('and_3v', T1, T2, T3), ('not_3v', T3, T4)]},
        # no dark gray thing is a sulfide
        { "syn": "vp(E1, T4) -> 'no' adj(E1, T1) 'thing' is() a() np(E1, T2)",
          "sem": lambda adj, is1, a, np: adj + np + [('and_3v', T1, T2, T3), ('not_3v', T3, T4)]},
        # gasoline is a fuel that burns
        { "syn": "vp(E1, T5) -> np(E1, T1) is() a() np(E1, T2) 'that' verb(E1, T3)",
          "sem": lambda np1, is1, a, np2, verb: np1 + np2 + verb + [('and', T1, T2, T4), ('and_3v', T3, T4, T5)] },


        # article
        { "syn": "a() -> 'a'", "sem": lambda: [] },
        { "syn": "a() -> 'an'", "sem": lambda: [] },

        # rel_clause
        { "syn": "rel_clause(E1, T1) -> 'that' verb(E1, T1)", "sem": lambda verb: verb },

        # verb
        { "syn": "verb(E1, T1) -> 'burns'", "sem": lambda: [('burns', E1, T1)] },
        { "syn": "verb(E1, T1) -> 'burns' 'rapidly'", "sem": lambda: [('burns_rapidly', E1, T1)] },

        # copula
        { "syn": "is() -> 'is'", "sem": lambda: [] },
        { "syn": "are() -> 'are'", "sem": lambda: [] },

        # np
        { "syn": "np(E1, T1) -> noun(E1, T1)", "sem": lambda noun: noun },
        { "syn": "np(E1, T1) -> adj(E1, T1) np(E1, T1)", "sem": lambda adj, noun: adj + noun },
        { "syn": "np(E1, T1) -> proper_noun(E1)", "sem": lambda proper_noun: proper_noun + [('=', T1, 'true')] },
        { "syn": "np(E1, T2) -> 'anything' 'that' is() 'not' a() np(E1, T1)", "sem": lambda is1, a, np: np + [('not_3v', T1, T2)] },

        # adjective
        { "syn": "adj(E1, T1) -> 'brittle'", "sem": lambda: [('brittle', E1, T1)] },
        { "syn": "adj(E1, T1) -> 'dark-gray'", "sem": lambda: [('dark_gray', E1, T1)] },

        # noun
        { "syn": "noun(E1, T1) -> 'metal'", "sem": lambda: [('metal', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'nonmetal'", "sem": lambda: [('nonmetal', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'compound'", "sem": lambda: [('compound', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'element'", "sem": lambda: [('element', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'white'", "sem": lambda: [('white', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'dark-gray'", "sem": lambda: [('dark_gray', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'oxide'", "sem": lambda: [('oxide', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'oxides'", "sem": lambda: [('oxide', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'sulfide'", "sem": lambda: [('sulfide', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'sulfides'", "sem": lambda: [('sulfide', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'brittle'", "sem": lambda: [('brittle', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'fuel'", "sem": lambda: [('fuel', E1, T1)] },

        # proper noun
        { "syn": "proper_noun(E1) -> /\w+/", "sem": lambda token: [('resolve_name', token, E1)] },
        { "syn": "proper_noun(E1) -> /\w+/ /\w+/", "sem": lambda token1, token2: [('resolve_name', token1 + " " + token2, E1)] },
    ]
