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
            # one day, ...
            "syn": "clause(C1) -> clause(C1) adverb(C1)",
            "sem": lambda clause, adverb: clause + adverb,
        },
        {
            "syn": "clause(C1) -> np(Sub) vp_sub(C1, Sub)",
            "sem": lambda np, vp_sub: apply(np, vp_sub)
        },
        {
            "syn": "clause(C1) -> clause(C1) 'and' clause(C2)",
            "sem": lambda clause1, clause2: clause1 + clause2,
        },
        {
            "syn": "clause(C1) -> np(Sub) vp_sub(C1, Sub) 'and' vp_sub(C2, Sub)",
            "sem": lambda np, vp_sub1, vp_sub2: apply(np, vp_sub1 + vp_sub2),
        },
        {
            "syn": "clause(C1) -> clause(C1)+','",
            "sem": lambda clause: clause,
        },
        # vp
        {
            "syn": "vp_sub(C1, Sub) -> 'was' past_participle_phase_sub(C1, Sub)",
            "sem": lambda past_participle_phase_sub: past_participle_phase_sub,
        },
        {
            "syn": "vp_sub(C1, Sub) -> iv(C1, Sub)",
            "sem": lambda iv: iv,
        },
        {
            "syn": "vp_sub(C1, Sub) -> 'had' past_participle_phase_sub(C1, Sub)",
            "sem": lambda past_participle_phase_sub: past_participle_phase_sub
        },
        # past participle phase
        {
            "syn": "past_participle_phase_sub(C1, Obj) -> past_participle_phase_sub_obj(C1, Sub, Obj) 'by' np(Sub)",
            "sem": lambda past_participle_phase_sub_obj, np: apply(np, past_participle_phase_sub_obj),
        },
        # {
        #     "syn": "past_participle_phase_sub_obj(C1, Sub, Obj) -> past_participle_phase_sub_obj(C1, Sub, Obj, Obj2)",
        #     "sem": lambda past_participle_phase_sub_obj: past_participle_phase_sub_obj,
        # },
        {
            "syn": "past_participle_phase_sub(C1, Sub) -> past_participle(C1, Sub)",
            "sem": lambda past_participle: past_participle,
        },
        {
            "syn": "past_participle_phase_sub(C1, Sub) -> adverb(C1) past_participle_phase_sub(C1, Sub)",
            "sem": lambda adverb, past_participle_phase_sub: adverb + past_participle_phase_sub,
        },

        {
            "syn": "past_participle_phase_sub(C1, Sub) -> past_participle_phase_sub_obj(C1, Sub, Obj) 'by' np(Obj)",
            "sem": lambda past_participle_phase_sub, np: apply(np, past_participle_phase_sub),
        },

        {
            "syn": "past_participle_phase_sub(C1, Sub) -> past_participle(C1, Sub, Obj) np(Obj)",
            "sem": lambda past_participle, np: apply(np, past_participle),
        },
        {
            "syn": "past_participle_phase_sub_obj(C1, Sub, Obj) -> past_participle(C1, Sub, Obj)",
            "sem": lambda past_participle: past_participle,
        },
        {
            "syn": "past_participle_phase_sub_obj(C1, Sub, Obj) -> past_participle(C1, Sub, Obj, Obj2) np(Obj2)",
            "sem": lambda past_participle: past_participle,
        },

        {
            "syn": "past_participle_phase_sub(C1, Sub) -> past_participle_phase_sub(C1, Sub, Obj) 'that' np(Obj)",
            "sem": lambda past_participle_phase_sub, np: apply(np, past_participle_phase_sub),
        },

        # {
        #     "syn": "clause_sub(C1, Sub) -> 'was' vp(C1, Sub)",
        #     "sem": lambda past_participle: past_participle,
        # },
        # {
        #     "syn": "clause_sub(C1, Sub) -> 'was' past_participle(C1, Sub)",
        #     "sem": lambda past_participle: past_participle,
        # },

        # {
        #     "syn": "clause_sub(C1) -> 'was' past_participle(C1, Sub, C2) subordinate_clause(C2)",
        #     "sem": lambda past_participle, subordinate_clause: past_participle + subordinate_clause,
        # },
        # {
        #     "syn": "subordinate_clause(C1) -> 'that' clause(C1)",
        #     "sem": lambda clause: clause,
        # },

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
        {
            "syn": "tv_sub_obj(C1, Sub, Obj) -> 'had' adverb(C1) past_participle(C1, Sub, Obj)",
            "sem": lambda adverb, past_participle: adverb + past_participle
        },
        # {
        #     "syn": "tv_sub_obj(E1, E2, E3) -> 'was' past_participle(E1, E2, E3) subordinate_clause(E3)",
        #     "sem": lambda past_participle, subordinate_clause: past_participle + subordinate_clause
        # },
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
            "syn": "past_participle(C1, Sub, Obj) -> 'told'",
            "sem": lambda: [('tell', C1, Sub, Obj)]
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
