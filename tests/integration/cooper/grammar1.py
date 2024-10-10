from richard.core.constants import E1, E2, E3, E4, E5, e1, e2, e3, Body, Range
from richard.entity.Variable import Variable
from richard.processor.parser.helper.grammar_functions import apply


T1 = Variable('T1')
T2 = Variable('T2')
T3 = Variable('T3')


def get_grammar1():
    return [
        # sentence

        # X is a Y
        {
            "syn": "s(E1) -> noun(E1, T1) is(E3) a(E4) np(E1, T1)",
            "sem": lambda noun, is1, a, np: [('=', T1, 'true')] + noun + [('store', np)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # no X is a Y
        {
            "syn": "s(E1) -> 'no' noun(E1, T1) is(E3) a(E4) np(E1, T2)",
            "sem": lambda noun, is1, a, np: [('=', T1, 'true'), ('=', T2, 'false'), ('learn_rule', np[0], noun)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # noun verb
        {
            "syn": "s(E1) -> noun(E1, T1) verb(E1)",
            "sem": lambda noun, verb: noun + [('store', verb)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },

        # np
        { "syn": "np(E1, T1) -> noun(E1, T1)", "sem": lambda noun: noun },
        { "syn": "np(E1, T1) -> adj(E1, T1) np(E1, T1)", "sem": lambda adj, noun: adj + noun },

        # verb
        { "syn": "verb(E1) -> 'burns' 'rapidly'", "sem": lambda: [('burns_rapidly', E1, 'true')] },

        # copula
        { "syn": "is(E1) -> 'is'", "sem": lambda: [] },

        # article
        { "syn": "a(E1) -> 'a'", "sem": lambda: [] },
        { "syn": "a(E1) -> 'an'", "sem": lambda: [] },

        # adjective
        { "syn": "adj(E1, T1) -> 'white'", "sem": lambda: [('white', E1, T1)] },
        { "syn": "adj(E1, T1) -> 'metallic'", "sem": lambda: [('metal', E1, T1)] },

        # noun
        { "syn": "noun(E1, T1) -> 'nonmetal'", "sem": lambda: [('nonmetal', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'metal'", "sem": lambda: [('metal', E1, T1)] },
        { "syn": "noun(E1, T1) -> 'element'", "sem": lambda: [('element', E1, T1)] },
        { "syn": "noun(E1, T1) -> proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },


        # proper noun
        { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },
    ]
