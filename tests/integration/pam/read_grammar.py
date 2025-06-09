import re
from richard.core.constants import E1, E2, E3, E4, e1, e2, e3, Body, Range
from richard.processor.parser.helper.grammar_functions import apply
from richard.type.SemanticFunction import SemanticFunction



def get_read_grammar():
    return [

        # sentence
        {
            "syn": "s(E1) -> s(E2) s(E3)",
            "sem": lambda s1, s2: s1 + s2,
        },
        {
            "syn": "clause(E1) -> 'one' 'day'+','? clause(E1)",
            "sem": lambda s: [],
        },
        {
            "syn": "clause(E1) -> 'john' 'went' 'through' 'a' 'red' 'light'",
            "sem": lambda: [],
        },
        {
            "syn": "clause(E1) -> 'john' 'had' 'just' 'gotten' 'a' 'summons for speeding by a cop the previous week,'",
            "sem": lambda: [],
        },
        {
            "syn": "clause(E1) -> 'was told that if he got another violation, his license would be taken away'",
            "sem": lambda: [],
        },
        {
            "syn": "clause(E1) -> 'then john remembered that he had two tickets for the giants\\' game on him'",
            "sem": lambda: [],
        },
        {
            "syn": "clause(E1) -> 'he told the cop that he would give them to him if he would forget the whole incident'",
            "sem": lambda: [],
        },
        {
            "syn": "clause(E1) -> 'the cop happened to be a terrific football fan'",
            "sem": lambda: [],
        },
        {
            "syn": "clause(E1) -> 'he took john\\'s tickets and drove away'",
            "sem": lambda: [],
        },

        {
            "syn": "clause(E1) -> clause(E2) 'and' clause(E3)",
            "sem": lambda s1, s2: s1 + s2,
        },
        {
            "syn": "clause(E1) -> 'was' 'pulled' 'over'",
            "sem": lambda: [],
        },
        {
            "syn": "s(E1) -> clause(E1)+'.'",
            "sem": lambda c: [],
        },
    ]
