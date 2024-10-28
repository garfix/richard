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
            "syn": "s(E1) -> noun(E1, T1) is() a() np(E1, T1)",
            "sem": lambda noun, is1, a, np: [('=', T1, 'true')] + noun + [('store', np)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # X is a Y that is Z
        {
            "syn": "s(E1) -> noun(E1, T1) is() a() np(E1, T1) 'that' is() np(E1, T1)",
            "sem": lambda noun, is1, a, np1, is2, np2: [('=', T1, 'true')] + noun + [('store', np1 + np2)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # no X is a Y
        {
            "syn": "s(E1) -> 'no' noun(E1, T1) is() a() np(E1, T2)",
            "sem": lambda noun, is1, a, np: [('=', T1, 'true'), ('=', T2, 'false'), ('learn_rule', np[0], noun)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # X is not a Y
        {
            "syn": "s(E1) -> a() noun(E1, T1) is() 'not' a() np(E1, T2)",
            "sem": lambda a1, noun, is1, a2, np: [('=', T1, 'true'), ('=', T2, 'false'), ('learn_rule', np[0], noun)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # noun verb
        {
            "syn": "s(E1) -> noun(E1, T1) verb(E1)",
            "sem": lambda noun, verb: noun + [('store', verb)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        {
            "syn": "s(E1) -> adj(E1, T1) 'things' verb(E1)",
            "sem": lambda adj, verb: [('=', T1, 'true'), ('=', T2, 'true'), ('learn_rule', verb[0], adj)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # dark-gray things are not white
        {
            "syn": "s(E1) -> adj(E1, T1) 'things' are() 'not' adj(E1, T2)",
            "sem": lambda adj1, are, adj2: [('=', T1, 'true'), ('=', T2, 'false'), ('learn_rule', adj2[0], adj1)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # gasoline is combustable
        {
            "syn": "s(E1) -> noun(E1, T1) 'is' adj(E1, T1)",
            "sem": lambda noun, adj: [('=', T1, 'true'), ('=', T2, 'true'), ('learn_rule', adj[0], noun)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # X is Y (X is another name for Y)
        {
            "syn": "s(E1) -> proper_noun(E1) 'is' proper_noun(E1)",
            "sem": lambda proper_noun1, proper_noun2: proper_noun1 + proper_noun2,
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # X's are not Y's
        {
            "syn": "s(E1) -> noun(E1, T1) are() 'not' np(E1, T2)",
            "sem": lambda noun, are, np: [
                ('scoped', [('=', T1, 'false'), ('=', T2, 'true'), ('learn_rule', noun[0], np)]),
                ('scoped', [('=', T1, 'true'), ('=', T2, 'false'), ('learn_rule', np[0], noun)])
            ],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # X's are Y's
        {
            "syn": "s(E1) -> noun(E1, T1) are() np(E1, T2)",
            "sem": lambda noun, are, np: [('=', T1, 'true'), ('=', T2, 'true'), ('learn_rule', np[0], noun)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },
        # any thing that burns rapidly burns
        {
            "syn": "s(E1) -> 'any' 'thing' 'that' verb(E1) verb(E1)",
            "sem": lambda verb1, verb2: [('=', T1, 'true'), ('=', T2, 'true'), ('learn_rule', verb2[0], verb1)],
            "inf": [("format", "canned"), ("format_canned", "OK")],
        },


        # np
        { "syn": "np(E1, T1) -> noun(E1, T1)", "sem": lambda noun: noun },
        { "syn": "np(E1, T1) -> adj(E1, T1) np(E1, T1)", "sem": lambda adj, noun: adj + noun },

        # verb
        { "syn": "verb(E1) -> 'burn'", "sem": lambda: [('burns', E1, 'true')] },
        { "syn": "verb(E1) -> 'burns'", "sem": lambda: [('burns', E1, 'true')] },
        { "syn": "verb(E1) -> 'burns' 'rapidly'", "sem": lambda: [('burns_rapidly', E1, 'true')] },
        { "syn": "verb(E1) -> 'rapidly' 'burns'", "sem": lambda: [('burns_rapidly', E1, 'true')] },

        # copula
        { "syn": "is() -> 'is'", "sem": lambda: [] },
        { "syn": "are() -> 'are'", "sem": lambda: [] },

        # article
        { "syn": "a() -> 'a'", "sem": lambda: [] },
        { "syn": "a() -> 'an'", "sem": lambda: [] },

        # adjective
        { "syn": "adj(E1, T1) -> 'white'", "sem": lambda: [('white', E1, T1)] },
        { "syn": "adj(E1, T1) -> 'dark' '-' 'gray'", "sem": lambda: [('dark_gray', E1, T1)] },
        { "syn": "adj(E1, T1) -> 'metallic'", "sem": lambda: [('metal', E1, T1)] },
        { "syn": "adj(E1, T1) -> 'combustable'", "sem": lambda: [('combustable', E1, T1)] },

        # noun
        { "syn": "noun(E1, T1) -> common_noun(E1, T1)", "sem": lambda common_noun: common_noun },
        { "syn": "noun(E1, T1) -> proper_noun(E1)", "sem": lambda proper_noun: proper_noun },

        # common noun
        { "syn": "common_noun(E1, T1) -> 'nonmetal'", "sem": lambda: [('nonmetal', E1, T1)] },
        { "syn": "common_noun(E1, T1) -> 'fuel'", "sem": lambda: [('fuel', E1, T1)] },
        { "syn": "common_noun(E1, T1) -> 'metal'", "sem": lambda: [('metal', E1, T1)] },
        { "syn": "common_noun(E1, T1) -> 'oxide'", "sem": lambda: [('oxide', E1, T1)] },
        { "syn": "common_noun(E1, T1) -> 'sulfide'", "sem": lambda: [('sulfide', E1, T1)] },
        { "syn": "common_noun(E1, T1) -> 'chloride'", "sem": lambda: [('chloride', E1, T1)] },
        { "syn": "common_noun(E1, T1) -> 'brittle'", "sem": lambda: [('brittle', E1, T1)] },
        { "syn": "common_noun(E1, T1) -> 'element'", "sem": lambda: [('element', E1, T1)] },
        { "syn": "common_noun(E1, T1) -> 'elements'", "sem": lambda: [('element', E1, T1)] },
        { "syn": "common_noun(E1, T1) -> 'compound'", "sem": lambda: [('compound', E1, T1)] },
        { "syn": "common_noun(E1, T1) -> 'compounds'", "sem": lambda: [('compound', E1, T1)] },

        # proper noun
        # "magnesium"
        { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: [('resolve_name', token, E1)] },
        # "ferrous sulfide"
        { "syn": "proper_noun(E1) -> token(E1) token(E1)", "sem": lambda token1, token2: [('resolve_name', token1 + " " + token2, E1)] },
        { "syn": "proper_noun(E1) -> token(E1) main_noun(E1)", "sem": lambda token, main_noun: [('resolve_name', token + ' ' + main_noun, E1)] },

        # the major part a compound noun
        { "syn": "main_noun(E1) -> 'oxide'", "sem": lambda: 'oxide', "inf": [("oxide", e1, 'true')] },
        { "syn": "main_noun(E1) -> 'chloride'", "sem": lambda: 'chloride', "inf": [("chloride", e1, 'true')] },
        { "syn": "main_noun(E1) -> 'sulfide'", "sem": lambda: 'sulfide', "inf": [("sulfide", e1, 'true')] },
    ]
