import re
from richard.core.constants import E1, E2, E3, E4, e1, e2, e3, Body, Range
from richard.processor.parser.helper.grammar_functions import apply
from richard.type.SemanticTemplate import SemanticTemplate



def get_read_grammar():
    return [

        # sentence
        {
            "syn": "s(E1) -> 'hello' 'world'",
            "sem": lambda: [('intent_hello',)],
        },
        {
            "syn": "s(E1) -> 'what' nbar(E1) 'are' 'there' + '?'",
            "sem": lambda nbar: [('intent_list', e1, nbar)],
        },

        # nbar
        { "syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun },

        # noun
        { "syn": "noun(E1) -> 'river'",         "sem": lambda: [('river', E1)],         "dialog": [('dialog_isa', e1, 'river')] },
        # plurals
        { "syn": "noun(E1) -> plural_noun(E1)'",    "sem": lambda plural_noun: plural_noun },
        { "syn": "plural_noun(E1) -> /\w+/+'s'",    "sem": lambda token: [(token, E1)], "dialog": lambda token: [('dialog_isa', e1, token)] },
    ]
