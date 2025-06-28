from richard.core.constants import Range, Body, E1, E2
from richard.entity.Variable import Variable
from richard.processor.parser.helper.grammar_functions import apply
from richard.type.SemanticFunction import SemanticFunction

C1 = Variable('C1')
C2 = Variable('C2')
Sub = Variable('Sub')
Obj = Variable('Obj')
Obj2 = Variable('Obj2')
X = Variable('X')



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
            # pre-adverb
            "syn": "clause(C1) -> adverb(C1)+','? clause(C1)",
            "sem": lambda adverb, clause: adverb + clause,
        },
        {
            # post-adverb
            "syn": "clause(C1) -> clause(C1) adverb(C1)",
            "sem": lambda clause, adverb: clause + adverb,
        },
        {
            # split clause in two
            "syn": "clause(C1) -> np(E1) clause(C1, E1)+','? 'and' clause(C2, E1)",
            "sem": lambda np, clause1, clause2: apply(np, clause1 + clause2),
        },
        {
            # split off first np
            "syn": "clause(C1) -> np(E1) clause(C1, E1)",
            "sem": lambda np, clause: apply(np, clause)
        },
        {
            # relative
            "syn": "relative_clause(C1) -> 'that' clause(C1)",
            "sem": lambda clause: clause
        },

        # clause expecting single argument
        {
            # post-adverb
            "syn": "clause(C1, E1) -> clause(C1, E1) adverb(C1)",
            "sem": lambda clause, adverb: clause + adverb,
        },
        {
            "syn": "clause(C1, E1) -> vp(C1, E1)",
            "sem": lambda verb: verb,
        },
        {
            "syn": "clause(C1, E1) -> vp(C1, E1, E2, E3)",
            "sem": lambda verb: verb,
        },
        {
            "syn": "clause(C1, E1) -> vp(C1, E1, C2) infinitival_clause(C2)",
            "sem": lambda verb, infinitival_clause: verb + infinitival_clause,
        },
        {
            "syn": "clause(C1, E1) -> vp(C1, X, E1, E2) np(E2)",
            "sem": lambda vp, np: apply(np, vp),
        },
        {
            "syn": "clause(C1, E1) -> vp(C1, E1, E3, E2) np(E2) 'to' np(E3)",
            "sem": lambda vp, np1, np2: apply(np1, apply(np2, vp)),
        },
        {
            "syn": "clause(C1, E1) -> vp(C1, X, E1, C2) relative_clause(C2)",
            "sem": lambda vp, relative_clause: vp + relative_clause,
        },
        {
            "syn": "clause(C1, E1) -> vp(C1, E1, E2, C2) np(E2) relative_clause(C2)",
            "sem": lambda vp, np, relative_clause: apply(np, vp + relative_clause),
        },
        {
            "syn": "clause(C1, E1) -> 'was' verb(C1, E1)",
            "sem": lambda verb: verb,
        },
        {
            "syn": "clause(C1, E1) -> 'was' vp(C1, X, E1, C2) relative_clause(C2)",
            "sem": lambda vp, relative_clause: vp + relative_clause,
        },
        {
            "syn": "clause(C1, E1) -> 'had' vp(C1, E1, E2, E3) np(E3) 'by' np(E2)",
            "sem": lambda vp, np1, np2: apply(np1, apply(np2, vp))
        },
        {
            # expression
            "syn": "clause(C1, E1) -> 'had' np(E2) 'on' 'him'",
            "sem": lambda np: apply(np, [('have_on_oneself', C1, E1, E2)])
        },
        {
            # conditional statement
            "syn": "clause(C1) -> 'if' clause(C2)+','? clause(C3)",
            "sem": lambda clause1, clause2: [('if', clause1, clause2)]
        },
        {
            # conditional statement
            "syn": "clause(C1) -> clause(C2)+','? 'if' clause(C3)",
            "sem": lambda clause1, clause2: [('if', clause2, clause1)]
        },
        {
            # infinitival statement
            "syn": "infinitival_clause(C1) -> 'to' 'be' np(E1)",
            "sem": lambda np: apply(np, [])
        },
        # verb phrase (just the verb and its modifiers, no np's)
        {
            "syn": "vp(C1, E1, E2, E3) -> adverb(C1) vp(C1, E1, E2, E3)",
            "sem": lambda adverb, clause: adverb + clause,
        },
        {
            "syn": "vp(C1, E1) -> verb(C1, E1)",
            "sem": lambda verb: verb
        },
        {
            "syn": "vp(C1, E1, E2) -> verb(C1, E1, E2)",
            "sem": lambda verb: verb
        },
        {
            "syn": "vp(C1, E1, E2, E3) -> verb(C1, E1, E2, E3)",
            "sem": lambda verb: verb
        },
        {
            "syn": "vp(C1, E1, E2, E3) -> 'would' 'be' verb(C1, E1, E2, E3)",
            "sem": lambda verb: verb
        },
        {
            "syn": "vp(C1, E1, E2, E3) -> 'would' verb(C1, E1, E2, E3)",
            "sem": lambda verb: verb
        },


# John had just gotten a summons for speeding by a cop the previous week,
# and was told that if he got another violation, his license would be taken away.
# Then John remembered that he had two tickets for the Giants' game on him.

        # np
        {
            "syn": "np(E1) -> 'his' nbar(E1)",
            "sem": lambda nbar: SemanticFunction([Body], nbar + [('his', E1)] + Body)
        },
        {
            "syn": "np(E1) -> 'he'",
            "sem": lambda: SemanticFunction([Body], [('he', E1)] + Body)
        },
        {
            "syn": "np(E1) -> 'him'",
            "sem": lambda: SemanticFunction([Body], [('he', E1)] + Body)
        },
        {
            "syn": "np(E1) -> 'them'",
            "sem": lambda: SemanticFunction([Body], [('them', E1)] + Body)
        },
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
            "syn": "np(E1) -> proper_noun(E1)",
            "sem": lambda proper_noun: SemanticFunction([Body], proper_noun + Body)
        },
        {
            "syn": "np(E1) -> np(E2)+'\\'' noun(E1)",
            "sem": lambda np, noun: SemanticFunction([Body], apply(np, noun + [('poss', E2, E1)]))
        },
        {
            "syn": "np(E1) -> np(E2)+'\\'s' noun(E1)",
            "sem": lambda np, noun: SemanticFunction([Body], apply(np, noun + [('poss', E2, E1)]))
        },

# !experiment!
# {
#     "syn": "noun(E1) -> proper_noun(E1) proper_noun(E2)",
#     "sem": lambda proper_noun, proper_noun2: proper_noun + proper_noun2,
# },
# {
#     "syn": "noun(E1) -> proper_noun(E1) proper_noun(E2) proper_noun(E3)",
#     "sem": lambda proper_noun, proper_noun2, proper_noun3: proper_noun + proper_noun2 + proper_noun3,
# },
        {
            "syn": "noun(E1) -> 'cop'",
            "sem": lambda: [('cop, E1')],
        },
        {
            "syn": "noun(E1) -> 'summons'",
            "sem": lambda: [('summons', E1)],
        },
        {
            "syn": "noun(E1) -> 'violation'",
            "sem": lambda: [('violation', E1)],
        },
        {
            "syn": "noun(E1) -> 'incident'",
            "sem": lambda: [('incident', E1)],
        },
        {
            "syn": "noun(E1) -> 'speeding'",
            "sem": lambda: [('speeding', E1)],
        },
        {
            "syn": "noun(E1) -> 'tickets'",
            "sem": lambda: [('ticket, E1')],
        },
        {
            "syn": "noun(E1) -> 'game'",
            "sem": lambda: [('game', E1)],
        },
        {
            "syn": "noun(E1) -> 'license'",
            "sem": lambda: [('license', E1)],
        },
        {
            "syn": "noun(E1) -> 'football' 'fan'",
            "sem": lambda: [('football_fan, E1')],
        },
        # proper noun
        {
            "syn": "proper_noun(E1) -> /\w+/",
            "sem": lambda token: [('resolve_name', token, E1)],
        },
        {
            "syn": "proper_noun(E1) -> 'the' /\w+/",
            "sem": lambda token: [('resolve_name', 'the ' + token, E1)],
        },
        # nbar
        {
            "syn": "nbar(E1) -> adjp(E1) nbar(E1)",
            "sem": lambda adjp, nbar: adjp + nbar
        },
        {
            "syn": "nbar(E1) -> nbar(E1) pp(E1)",
            "sem": lambda nbar, pp: nbar + pp
        },
        {
            "syn": "nbar(E1) -> noun(E1)",
            "sem": lambda noun: noun,
        },
        # adjp
        {
            "syn": "adjp(E1) -> adj(E1)",
            "sem": lambda adj: adj,
        },
        # adjective
        {
            "syn": "adj(E1) -> 'another'",
            "sem": lambda: [('another', E1)],
        },
        {
            "syn": "adj(E1) -> 'whole'",
            "sem": lambda: [('whole', E1)],
        },
        {
            "syn": "adj(E1) -> 'terrific'",
            "sem": lambda: [('terrific', E1)],
        },
        # det
        {
            "syn": "det(E1) -> 'the'",
            "sem": lambda: SemanticFunction([Range, Body], Range + Body)
        },
        {
            "syn": "det(E1) -> 'a'",
            "sem": lambda: SemanticFunction([Range, Body], Range + Body)
        },
        {
            "syn": "det(E1) -> number(E1)",
            "sem": lambda number: SemanticFunction([Range, Body], [('det_equals', Range + Body, number)])
        },
        # verb
        {
            "syn": "verb(C1, Sub, Obj) -> 'happened'",
            "sem": lambda: [('happen', C1, Sub, Obj)]
        },
        {
            "syn": "verb(C1, Sub, Obj, Obj2) -> 'give'",
            "sem": lambda: [('give', C1, Sub, Obj, Obj2)]
        },
        {
            "syn": "verb(C1, Sub, Obj, Obj2) -> 'forget'",
            "sem": lambda: [('forget', C1, Sub, Obj, Obj2)]
        },
        {
            "syn": "verb(C1, Sub, Obj, Obj2) -> 'remembered'",
            "sem": lambda: [('remember', C1, Sub, Obj, Obj2)]
        },
        {
            "syn": "verb(C1, Sub, Obj, Obj2) -> 'got'",
            "sem": lambda: [('get', C1, Sub, Obj, Obj2)]
        },
        {
            "syn": "verb(C1, Sub, Obj, Obj2) -> 'gotten'",
            "sem": lambda: [('get', C1, Sub, Obj, Obj2)]
        },
        {
            "syn": "verb(C1, Sub, Obj, Obj2) -> 'took'",
            "sem": lambda: [('take', C1, Sub, Obj, Obj2)]
        },
        {
            "syn": "verb(C1, Sub, Obj, Obj2) -> 'taken' 'away'",
            "sem": lambda: [('take_away', C1, Sub, Obj, Obj2)]
        },
        {
            "syn": "verb(C1, Sub, Obj, Obj2) -> 'drove' 'away'",
            "sem": lambda: [('drive_away', C1, Sub, Obj, Obj2)]
        },
        {
            "syn": "verb(C1, Sub, Obj, Obj2) -> 'told'",
            "sem": lambda: [('tell', C1, Sub, Obj, Obj2)]
        },
        {
            "syn": "verb(C1, Sub) -> 'pulled' 'over'",
            "sem": lambda: [('pull_over', C1, Sub, X)],
        },
        {
            "syn": "verb(C1, Sub) -> go() 'through' 'a' 'red' 'light'",
            "sem": lambda go: [('go_through_red_light', C1, Sub)],
        },
        {
            "syn": "go() -> 'went'",
            "sem": lambda: []
        },
        # adverb
        {
            "syn": "adverb(E1) -> 'then'",
            "sem": lambda: []
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
            "syn": "adverb(E1) -> 'the'? 'previous' 'week'",
            "sem": lambda: [('previous_week', E1)]
        },
        # preposition phase
        {
            "syn": "pp(E1) -> prep(E1, E2) np(E2)",
            "sem": lambda prep, np: apply(np, prep)
        },
        # preposition
        {
            "syn": "prep(E1, E2) -> 'for'",
            "sem": lambda: [('for', E1, E2)]
        },
        # number
        {
            "syn": "number(E1) -> 'two'",
            "sem": lambda: 2
        },



        # === DONE ^ =============================
        {
            "syn": "clause(E1) -> 'why did' np(E2) 'offer the cop a couple of tickets'",
            "sem": lambda np: [],
        },


    ]
