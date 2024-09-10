from richard.core.constants import E1, E2, e2, Body
from richard.processor.parser.helper.grammar_functions import apply
from richard.type.SemanticTemplate import SemanticTemplate


def get_grammar():
    return [

        # sentence
        {
            "syn": "s(E2) -> 'where' 'was' np(E1) 'born' '?'",
            "sem": lambda np: apply(np, []) + [('place_of_birth', E1, E2)],
            "inf": [("format", "list"), ("format_list", e2)],
        },

        # nbar
        { "syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun },

        # np
        { "syn": "np(E1) -> nbar(E1)", "sem": lambda nbar:
            SemanticTemplate([Body], nbar + Body) },

        # noun
        { "syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },

        # proper noun
        { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },
    ]
