from richard.core.constants import Range, Body, E1, E2
from richard.entity.Variable import Variable
from richard.processor.parser.helper.grammar_functions import apply
from richard.type.SemanticFunction import SemanticFunction

C1 = Variable('C1')
C2 = Variable('C2')
Sub = Variable('Sub')
Obj = Variable('Obj')
Obj2 = Variable('Obj2')


def get_read_grammar():
    return [

        # question
        {
            "syn": "s() -> paragraph()",
            "sem": lambda paragraph: paragraph + [('intent_understood',)],
        },
        {
            "syn": "paragraph() -> s(E1)",
            "sem": lambda s: s,
        },
        {
            "syn": "paragraph() -> s(E1) paragraph()",
            "sem": lambda s, paragraph: s + paragraph,
        },
        {
            "syn": "s() -> clause(C1)+'?'",
            "sem": lambda clause: clause + [('intent_question',)],
        },
        # story of declarative sentences
        {
            "syn": "s() -> story()",
            "sem": lambda paragraph: paragraph + [('intent_understood',)],
        },
        {
            "syn": "story() -> decl(C1) story()",
            "sem": lambda decl, paragraph: decl + paragraph,
        },
        {
            "syn": "story() -> decl(C1)",
            "sem": lambda decl: decl,
        },
        # declarative
        {
            "syn": "decl(C1) -> clause(C1)+'.'",
            "sem": lambda clause: [],
        },
        # clause
        # - refer to all verb phrases as the generic 'vp'
        {
            # one day, ...
            "syn": "clause(C1) -> adverb(C1)+','? clause(C1)",
            "sem": lambda adverb, clause: adverb + clause,
        },
        {
            "syn": "clause(C1) -> np(E1) vp(C1, E1)",
            "sem": lambda np, vp_sub: apply(np, vp_sub)
        },
        {
            "syn": "clause(C1) -> np(E1) vp(C1, E1) 'and' vp(C2, E1)",
            "sem": lambda np, vp1, vp2: apply(np, vp1 + vp2),
        },
        # subordinate_clause
        {
            "syn": "subordinate_clause(C1) -> 'that' clause(C1)",
            "sem": lambda clause: clause,
        },
        # vp
        {
            "syn": "vp(C1, E1) -> vp(C1, E1)+','",
            "sem": lambda clause: clause,
        },
        {
            "syn": "vp(C1, E1) -> vp(C1, E1) adverb(C1)",
            "sem": lambda clause, adverb: clause + adverb,
        },
        {
            "syn": "vp(C1, E1) -> 'was' vp(C1, E1)",
            "sem": lambda vp: vp,
        },
        {
            "syn": "vp(C1, E1) -> iv(C1, E1)",
            "sem": lambda iv: iv,
        },
        {
            "syn": "vp(C1, E1, E2, E3) -> past_participle(C1, E1, E2, E3)",
            "sem": lambda past_participle: past_participle,
        },
        {
            "syn": "vp(C1, E1) -> past_participle(C1, E1, E2)",
            "sem": lambda past_participle: past_participle,
        },
        {
            "syn": "vp(C1, E2) -> vp(C1, E1, E2, E3) np(E3) 'by' np(E1)",
            "sem": lambda vp, np1, np2: apply(np1, apply(np2, vp)),
        },
        {
            # had just gotten a summons
            "syn": "vp(C1, E1) -> 'had' vp(C1, E1)",
            "sem": lambda vp: vp
        },
        {
            # had just gotten a summons
            "syn": "vp(C1, E1) -> adverb(C1) vp(C1, E1)",
            "sem": lambda adverb, vp: adverb + vp
        },



        # np
        {
            "syn": "np(E1) -> nbar(E1)",
            "sem": lambda nbar: SemanticFunction([Body], nbar + Body)
        },
        {
            "syn": "np(E1) -> det(E1) nbar(E1)",
            "sem": lambda det, nbar: SemanticFunction([Body], apply(det, nbar, Body))
        },
        # noun
        {
            "syn": "noun(E1) -> proper_noun(E1)",
            "sem": lambda proper_noun: proper_noun,
        },
        {
            "syn": "noun(E1) -> 'cop'",
            "sem": lambda: [('cop, E1')],
        },
        {
            "syn": "noun(E1) -> 'summons'",
            "sem": lambda: [('summons', E1)],
        },
        {
            "syn": "noun(E1) -> 'speeding'",
            "sem": lambda: [('speeding', E1)],
        },
        # proper noun
        {
            "syn": "proper_noun(E1) -> /\w+/",
            "sem": lambda token: [('resolve_name', token, E1)],
        },
        # nbar
        {
            "syn": "nbar(E1) -> nbar(E1) pp(E1)",
            "sem": lambda nbar, pp: nbar + pp
        },
        {
            "syn": "nbar(E1) -> noun(E1)",
            "sem": lambda noun: noun,
        },
        # det
        {
            "syn": "det(E1) -> 'a'",
            "sem": lambda: SemanticFunction([Range, Body], Range + Body)
        },
        # verb
        {
            "syn": "iv(C1, Sub) -> go() 'through' 'a' 'red' 'light'",
            "sem": lambda go: [('go_through_red_light', C1, Sub)],
        },
        # adverb
        {
            "syn": "adverb(E1) -> 'just'",
            "sem": lambda: []
        },
        {
            "syn": "adverb(E1) -> 'one day'",
            "sem": lambda: []
        },
        {
            "syn": "adverb(E1) -> 'the'? 'previous' 'week'",
            "sem": lambda: [('previous_week', E1)]
        },
        # verb inflections
        {
            "syn": "go() -> 'went'",
            "sem": lambda: []
        },
        {
            "syn": "past_participle(C1, Sub, Obj, Obj2) -> 'gotten'",
            "sem": lambda: [('get', C1, Sub, Obj, Obj2)]
        },
        {
            "syn": "past_participle(C1, Sub, Obj, Obj2) -> 'told'",
            "sem": lambda: [('tell', C1, Sub, Obj, Obj2)]
        },
        {
            "syn": "past_participle(C1, Sub, Obj) -> 'pulled' 'over'",
            "sem": lambda: [('pull_over', C1, Sub, Obj)],
        },
        # preposition phase
        {
            "syn": "pp(E1) -> prep(E1, E2) noun(E2)",
            "sem": lambda prep, noun: prep + noun
        },
        {
            "syn": "pp(E1) -> prep(E1, E2) np(E2)",
            "sem": lambda prep, np: apply(np, prep)
        },
        # preposition
        {
            "syn": "prep(E1, E2) -> 'for'",
            "sem": lambda: [('for', E1, E2)]
        },



        # === DONE ^ =============================
        {
            "syn": "clause(E1) -> clause_sub(E1) 'if he got another violation, his license would be taken away'",
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
            "syn": "clause(E1) -> 'why did' np(E2) 'offer the cop a couple of tickets'",
            "sem": lambda np: [],
        },


    ]
