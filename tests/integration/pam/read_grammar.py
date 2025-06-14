from richard.core.constants import E1, E2, E3, E4, e1, e2, e3, Body, Range
from richard.processor.parser.helper.grammar_functions import apply
from richard.type.SemanticFunction import SemanticFunction



def get_read_grammar():
    return [

        # sentence
        {
            "syn": "s(E1) -> s(E2) s(E3)",
            "sem": lambda s1, s2: s1 + s2 + [('intent_understood',)],
        },
        {
            # one day, ...
            "syn": "clause(E1) -> adverb(E1)+','? clause(E1)",
            "sem": lambda adverb, clause: adverb + clause,
        },
        {
            "syn": "clause(E1) -> np(E1) iv(E2, E1)",
            "sem": lambda np, iv: apply(np, iv)
        },
        {
            "syn": "clause(E1) -> np(E2) tv_sub_obj(E1, E2, E3) np(E3)",
            "sem": lambda np1, tv_sub_obj, np2: apply(np1, apply(np2, tv_sub_obj)),
        },
        {
            "syn": "iv(E1, E2) -> go() 'through' 'a' 'red' 'light'",
            "sem": lambda go: [('go_through_red_light', E1, E2)],
        },
        {
            "syn": "np(E1) -> nbar(E1)",
            "sem": lambda nbar: SemanticFunction([Body], nbar + Body)
        },
        {
            "syn": "np(E1) -> det(E1) nbar(E1)",
            "sem": lambda det, nbar: SemanticFunction([Body], apply(det, nbar, Body))
        },
        {
            "syn": "nbar(E1) -> nbar(E1) adjp(E1)",
            "sem": lambda nbar, adjp: nbar + adjp
        },
        {
            "syn": "det(E1) -> 'a'",
            "sem": lambda: SemanticFunction([Range, Body], Range + Body)
        },
        {
            "syn": "tv_sub_obj(E1, E2, E3) -> 'had' adverb(E1) past_participle(E1, E2, E3)",
            "sem": lambda adverb, past_participle: adverb + past_participle
        },
        {
            "syn": "tv_sub_obj(E1, E2, E3) -> 'had' past_participle(E1, E2, E3)",
            "sem": lambda past_participle: past_participle
        },
        {
            "syn": "adverb(E1) -> 'just'",
            "sem": lambda: []
        },
        {
            "syn": "adverb(E1) -> 'one day'",
            "sem": lambda: []
        },
        {
            "syn": "go() -> 'went'",
            "sem": lambda: []
        },
        {
            "syn": "past_participle(E1, E2, E3) -> 'gotten'",
            "sem": lambda: [('get', E1, E2, E3)]
        },
        # === DONE ^ =============================
        {
            "syn": "adjp(E1) -> 'for speeding by a cop the previous week,'",
            "sem": lambda: []
        },
        {
            "syn": "clause(E1) -> 'was told that if he got another violation, his license would be taken away'",
            "sem": lambda: [],
        },
        {
            "syn": "clause(E1) -> 'then' np(E2) 'remembered that he had two tickets for the giants\\' game on him'",
            "sem": lambda np: [],
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
            "syn": "clause(E1) -> 'he took' np(E2)+'\\'s tickets and drove away'",
            "sem": lambda np: [],
        },
        {
            "syn": "clause(E1) -> clause(E2) 'and' clause(E3)",
            "sem": lambda s1, s2: s1 + s2,
        },
        {
            "syn": "clause(E1) -> 'was' past_participle(E1)",
            "sem": lambda past_participle: past_participle,
        },
        {
            "syn": "past_participle(E1) -> 'pulled' 'over'",
            "sem": lambda: [('pull_over', E1)],
        },
        {
            "syn": "s(E1) -> clause(E1)+'.'",
            "sem": lambda c: [],
        },
        {
            "syn": "s(E1) -> clause(E1)+'?'",
            "sem": lambda clause: clause + [('intent_question',)],
        },
        {
            "syn": "clause(E1) -> 'why did' np(E2) 'offer the cop a couple of tickets'",
            "sem": lambda np: [],
        },
        {
            "syn": "nbar(E1) -> noun(E1)",
            "sem": lambda noun: noun,
        },
        {
            "syn": "noun(E1) -> proper_noun(E1)",
            "sem": lambda proper_noun: proper_noun,
        },
        {
            "syn": "noun(E1) -> 'summons'",
            "sem": lambda: [('summons', E1)],
        },
        {
            "syn": "proper_noun(E1) -> /\w+/",
            "sem": lambda token: [('resolve_name', token, E1)],
        },

    ]
