from richard.core.constants import E1, E2, E3, E4, E5, e1, e2, e3, Body, Range
from richard.entity.Variable import Variable
from richard.processor.parser.helper.grammar_functions import apply


T1 = Variable('T1')
T2 = Variable('T2')
T3 = Variable('T3')


def get_read_grammar1():
    return [
        # sentence

        # introduce new names
        # X is a Y
        {
            "syn": "s() -> proper_noun(E1) is() a() np(E1, T1)",
            "sem": lambda noun, is1, a, np: [('let', T1, 'true')] + noun + [('sentence_tell', np)],
        },
        # X is Y (X is another name for Y)
        {
            "syn": "s() -> proper_noun(E1) 'is' proper_noun(E1)",
            "sem": lambda proper_noun1, proper_noun2: [('sentence_tell', proper_noun1 + proper_noun2)],
        },

        # no X is a Y
        {
            "syn": "s() -> 'no' noun(E1, T1) is() a() np(E1, T2)",
            "sem": lambda noun, is1, a, np: [('let', T1, 'true'), ('let', T2, 'false'), ('sentence_learn', np[0], noun)],
        },
        # a X is not a Y
        {
            "syn": "s() -> a() noun(E1, T1) is() 'not' a() np(E1, T2)",
            "sem": lambda a1, noun, is1, a2, np: [('let', T1, 'true'), ('let', T2, 'false'), ('sentence_learn', np[0], noun)],
        },


        # noun verb
        {
            "syn": "s() -> noun(E1, T1) verb(E1)",
            "sem": lambda noun, verb: noun + [('store', verb)],
        },
        # combustable things burn
        {
            "syn": "s() -> np(E1, T1) verb(E1)",
            "sem": lambda np, verb: [('let', T1, 'true'), ('let', T2, 'true'), ('sentence_learn', verb[0], np)],
        },


        # dark-gray things are not white
        {
            "syn": "s() -> np(E1, T1) are() 'not' adj(E1, T2)",
            "sem": lambda np, are, adj2: [('let', T1, 'true'), ('let', T2, 'false'), ('sentence_learn', adj2[0], np)],
        },
        # gasoline is combustable
        {
            "syn": "s() -> noun(E1, T1) 'is' adj(E1, T1)",
            "sem": lambda noun, adj: [('let', T1, 'true'), ('let', T2, 'true'), ('sentence_learn', adj[0], noun)],
        },
        # X's are not Y's
        {
            "syn": "s() -> noun(E1, T1) are() 'not' np(E1, T2)",
            "sem": lambda noun, are, np: [
                ('scoped', [('let', T1, 'false'), ('let', T2, 'true'), ('sentence_learn', noun[0], np)]),
                ('scoped', [('let', T1, 'true'), ('let', T2, 'false'), ('sentence_learn', np[0], noun)])
            ],
        },
        # X's are Y's
        {
            "syn": "s() -> noun(E1, T1) are() np(E1, T2)",
            "sem": lambda noun, are, np: [('let', T1, 'true'), ('let', T2, 'true'), ('sentence_learn', np[0], noun)],
        },
        # any thing that burns rapidly burns
        {
            "syn": "s() -> 'any' 'thing' 'that' verb(E1) verb(E1)",
            "sem": lambda verb1, verb2: [('let', T1, 'true'), ('let', T2, 'true'), ('sentence_learn', verb2[0], verb1)],
        },


        # np
        { "syn": "np(E1, T1) -> noun(E1, T1)", "sem": lambda noun: noun },
        { "syn": "np(E1, T1) -> adj(E1, T1) np(E1, T1)", "sem": lambda adj, noun: adj + noun },
        { "syn": "np(E1, T1) -> np(E1, T1) 'that' 'is' np(E1, T1)", "sem": lambda np1, np2: np1 + np2 },

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
        { "syn": "adj(E1, T1) -> 'dark-gray'", "sem": lambda: [('dark_gray', E1, T1)] },
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
        { "syn": "common_noun(E1, T1) -> 'things'", "sem": lambda: [] },

        # proper noun
        # "magnesium"
        { "syn": "proper_noun(E1) -> /\w+/", "sem": lambda token: [('resolve_name', token, E1)] },
        # "ferrous sulfide"
        { "syn": "proper_noun(E1) -> /\w+/ /\w+/", "sem": lambda token1, token2: [('resolve_name', token1 + " " + token2, E1)] },
        { "syn": "proper_noun(E1) -> /\w+/ main_noun(E1)", "sem": lambda token, main_noun: [('resolve_name', token + ' ' + main_noun, E1)] },

        # the major part a compound noun
        { "syn": "main_noun(E1) -> 'oxide'", "sem": lambda: 'oxide', "dialog": [("oxide", e1, 'true')] },
        { "syn": "main_noun(E1) -> 'chloride'", "sem": lambda: 'chloride', "dialog": [("chloride", e1, 'true')] },
        { "syn": "main_noun(E1) -> 'sulfide'", "sem": lambda: 'sulfide', "dialog": [("sulfide", e1, 'true')] },
    ]
