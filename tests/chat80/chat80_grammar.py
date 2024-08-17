import re
from richard.constants import E1, E2, E3, E4, Body, Range
from richard.processor.parser.helper.grammar_functions import apply
from richard.type.SemanticTemplate import SemanticTemplate



def get_grammar():
    return [

        # sentence
        { 
            "syn": "s(E1) -> 'does' np(E1) vp_nosub_obj(E1) '?'",  
            "sem": lambda np, vp_nosub_obj: apply(np, vp_nosub_obj), 
            "inf": [("format", "y/n")],
        },
        { 
            "syn": "s(E1) -> 'is' 'there' np(E1) '?'",  
            "sem": lambda np: apply(np, []), 
            "inf": [("format", "y/n")],        
        },
        { 
            "syn": "s(E2) -> 'is' 'there' np(E1) preposition(E1, E2) 'each' nbar(E2) '?'",  
            "sem": lambda np, preposition, nbar: [('all', E2, nbar, apply(np, preposition))], 
            "inf": [("format", "y/n")], 
        },
        { 
            "syn": "s(E1) -> 'what' nbar(E1) 'are' 'there' '?'", 
            "sem": lambda nbar: nbar, 
            "inf": [("format", "list", E1)],
        },
        { 
            "syn": "s(E1) -> 'what' nbar(E1) 'are' 'there' pp(E1) '?'", 
            "sem": lambda nbar, pp: nbar + pp, 
            "inf": [("format", "list", E1)],
        },
        { 
            "syn": "s(E1) -> 'what' 'is' np(E1) '?'", 
            "sem": lambda np: apply(np, []), 
            "inf": [("format", "list", E1)],
        },
        { 
            "syn": "s(E1) -> 'what' 'are' np(E1) '?'", 
            "sem": lambda np: apply(np, []), 
            "inf": [("format", "list", E1)],
        },
        { 
            "syn": "s(E1) -> 'what' 'are' np(E1) vp_noobj_sub_iob(E1) '?'", 
            "sem": lambda np, vp_noobj_sub_iob: apply(np, vp_noobj_sub_iob),
            "inf": [("format", "list", E1)],
        },
        { 
            "syn": "s(E1) -> 'what' 'are' 'the' noun(E1) 'of' np(E2) '?'", 
            "sem": lambda noun, np: noun + [('of', E1, E2)] + apply(np, []),
            "inf": [("format", "table", [E2, E1], [None, None])],
            "boost": 1
        },
        { 
            "syn": "s(E1) -> 'what' 'is' 'the' 'total' 'area' 'of' np(E2) '?'", 
            "sem": lambda np: [("sum", E1, E3, apply(np, []) + [('size_of', E2, E3)])],
            "inf": [("format", "number", E1, "ksqmiles")],
        },
        { 
            "syn": "s(E1) -> 'what' 'is' 'the' 'average' 'area' 'of' np(E2) preposition(E2, E3) 'each' nbar(E3) '?'", 
            "sem": lambda np, preposition, nbar: nbar + [('avg', E1, E4, apply(np, preposition) + [('size_of', E2, E4)])],
            "inf": [("format", "table", [E3, E1], [None, 'ksqmiles'])],
        },
        { 
            "syn": "s(E1) -> 'what' 'percentage' 'of' np(E1) tv(E1, E2) 'each' nbar(E2) '?'", 
            "sem": lambda np, tv, nbar: nbar + [('percentage', E3, apply(np, tv), apply(np, []))], 
            "inf": [("format", "table", [E2, E3], [None, None])],
        },
        { 
            "syn": "s(E2) -> 'where' 'is' np(E1) '?'", 
            "sem": lambda np: apply(np, []) + [('where', E1, E2)], 
            "inf": [("format", "list", E2)],
        },
        { 
            "syn": "s(E2) -> 'how' 'large' 'is' np(E1) '?'",  
            "sem": lambda np: apply(np, []) + [('size_of', E1, E2)],
            "inf": [("format", "number", E2, "ksqmiles")],
        },
        { 
            "syn": "s(E1) -> 'which' nbar(E1) 'are' adjp(E1) '?'", 
            "sem": lambda nbar, adjp: nbar + adjp, 
            "inf": [("format", "list", E1)],
        },
        { 
            "syn": "s(E1) -> 'which' nbar(E1) 'are' vp_noobj_sub(E1) '?'", 
            "sem": lambda nbar, vp_noobj_sub: nbar + vp_noobj_sub,
            "inf": [("format", "list", E1)],
        },
        { 
            "syn": "s(E1) -> 'which' 'is' np(E1) '?'", 
            "sem": lambda np: apply(np, []), 
            "inf": [("format", "list", E1)],
        },
        { 
            "syn": "s(E1) -> 'which' nbar(E1) '\\'' 's' np(E2) 'is' np(E3) '?'", 
            "sem": lambda nbar, np1, np2: nbar + apply(np1, [('of', E2, E1)] + apply(np2, [('==', E2, E3)])),
            "inf": [("format", "list", E1)],
        },
        { 
            "syn": "s(E1) -> 'which' np(E1) vp_nosub_obj(E1) '?'", 
            "sem": lambda np, vp_nosub_obj: apply(np, vp_nosub_obj),
            "inf": [("format", "list", E1)],
        },
        { 
            "syn": "s(E1) -> 'how' 'many' nbar(E2) vp_noobj_sub(E2) '?'", 
            "sem": lambda nbar, vp_noobj_sub: [('count', E1, nbar + vp_noobj_sub)], 
            "inf": [("format", "number", E1, None)],
        },
        { 
            "syn": "s(E1) -> 'bye' '.'", 
            "sem": lambda: [('=', E1, 'Cheerio.')], 
            "inf": [("format", "list", E1)],
        },


        # active transitive: sub obj
        { "syn": "vp_nosub_obj(E1) -> vp_nosub_noobj(E1, E2) np(E2)", "sem": lambda vp_nosub_noobj, np: apply(np, vp_nosub_noobj) },
        { "syn": "vp_nosub_obj(E1) -> 'does' 'not' vp_nosub_noobj(E1, E2) np(E2)", "sem": lambda vp_nosub_noobj, np: [('not', apply(np, vp_nosub_noobj))] },
        { "syn": "vp_nosub_noobj(E1, E2) -> tv(E1, E2)", "sem": lambda tv: tv },

        { "syn": "vp_nosub_obj(E1) -> 'have' 'a' attr(E1, E2)", "sem": lambda attr: attr },

        # passive transitive
        { "syn": "vp_noobj_sub(E1) -> tv(E2, E1) 'by' np(E2)", "sem": lambda tv, np: apply(np, tv) },
        { "syn": "vp_noobj_sub(E1) -> 'does' np(E2) tv(E2, E1)", "sem": lambda np, tv: apply(np, tv) },
        { "syn": "vp_noobj_sub(E1) -> 'is' tv(E2, E1) 'by' np(E2)", "sem": lambda tv, np: apply(np, tv) },

        # active transitive continuous
        { "syn": "vp_nosub_obj_continuous(E1) -> tv_continuous(E1, E2) np(E2)", "sem": lambda tv_continuous, np: apply(np, tv_continuous) },

        # passive ditransitive: obj sub iob
        { "syn": "vp_noobj_sub_iob(E1) -> 'from' 'which' np(E2) vp_noobj_nosub_iob(E1, E2)", "sem": lambda np, vp_noobj_nosub_iob: apply(np, vp_noobj_nosub_iob) },
        { "syn": "vp_noobj_nosub_iob(E1, E2) -> dtv(E2, E1, E3) np(E3)", "sem": lambda dtv, np: apply(np, dtv) },

        # transitive verbs
        { "syn": "tv(E1, E2) -> 'border'", "sem": lambda: [('borders', E1, E2)] },
        { "syn": "tv(E1, E2) -> 'borders'", "sem": lambda: [('borders', E1, E2)] },
        { "syn": "tv(E1, E2) -> 'bordered'", "sem": lambda: [('borders', E1, E2)] },
        { "syn": "tv(E1, E2) -> 'contains'", "sem": lambda: [('contains', E1, E2)] },
        { "syn": "tv(E1, E2) -> 'flow' 'through'", "sem": lambda: [('flows_through', E1, E2)] },
        { "syn": "tv(E1, E2) -> 'exceeds'", "sem": lambda: [('>', E1, E2)] },

        { "syn": "tv_continuous(E1, E2) -> 'bordering'", "sem": lambda: [('borders', E1, E2)] },
        { "syn": "tv_continuous(E1, E2) -> 'exceeding'", "sem": lambda: [('>', E1, E2)] },

        # ditransitive verbs
        { "syn": "dtv(E1, E2, E3) -> 'flows' 'into'", "sem": lambda: [('flows_from_to', E1, E2, E3)] },

        # nbar
        { "syn": "nbar(E1) -> adj(E1) nbar(E1)", "sem": lambda adj, nbar: adj + nbar },
        { "syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun },
        { "syn": "nbar(E1) -> nbar(E1) pp(E1)", "sem": lambda nbar, pp: nbar + pp },
        { "syn": "nbar(E1) -> superlative(E1) nbar(E1)", "sem": lambda superlative, nbar: apply(superlative, nbar) },
        { "syn": "nbar(E1) -> nbar(E1) relative_clause(E1)", "sem": lambda nbar, relative_clause: nbar + relative_clause },
        { "syn": "nbar(E1) -> nbar(E1) pp(E1)", "sem": lambda nbar, pp: nbar + pp },

        # relative clauses
        { "syn": "relative_clause(E1) -> 'that' vp_nosub_obj(E1)", "sem": lambda vp_nosub_obj: vp_nosub_obj },
        { "syn": "relative_clause(E1) -> 'that' vp_noobj_sub(E1)", "sem": lambda vp_noobj_sub: vp_noobj_sub },
        { "syn": "relative_clause(E1) -> relative_clause(E1) 'and' relative_clause(E1)", "sem": lambda relative_clause1, relative_clause2: relative_clause1 + relative_clause2 },
        { "syn": "relative_clause(E1) -> vp_nosub_obj_continuous(E1)", "sem": lambda vp_nosub_obj: vp_nosub_obj },
        { "syn": "relative_clause(E1) -> np(E2) preposition(E2, E1) 'which' vp_nosub_obj(E2)", "sem": lambda np, preposition, vp_nosub_obj: apply(np, preposition + vp_nosub_obj) },
        { "syn": "relative_clause(E1) -> 'whose' attr(E1, E2) vp_nosub_obj(E2)", "sem": lambda attr, vp_nosub_obj: attr + vp_nosub_obj },
        { "syn": "relative_clause(E1) -> 'with' 'a' attr(E1, E2) vp_nosub_obj_continuous(E2)", "sem": lambda attr, vp_nosub_obj: attr + vp_nosub_obj },

        # np
        { "syn": "np(E1) -> nbar(E1)", "sem": lambda nbar: 
            SemanticTemplate([Body], nbar + Body) },
        { "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar: 
            SemanticTemplate([Body], apply(det, nbar, Body)) },
        { "syn": "np(E1) -> det(E1) attr(E2, E1) 'of' nbar(E2)", "sem": lambda det, attr, nbar: 
            SemanticTemplate([Body], apply(det, nbar + attr, Body)) },
        { "syn": "np(E1) -> number(E1)", "sem": lambda number: 
            SemanticTemplate([Body], [('=', E1, number)] + Body) },

        # det
        { "syn": "det(E1) -> 'a'", "sem": lambda: 
            SemanticTemplate([Range, Body], Range + Body) },
        { "syn": "det(E1) -> 'the'", "sem": lambda: 
            SemanticTemplate([Range, Body], Range + Body) },
        { "syn": "det(E1) -> 'some'", "sem": lambda: 
            SemanticTemplate([Range, Body], Range + Body) },
        { "syn": "det(E1) -> 'any'", "sem": lambda: 
            SemanticTemplate([Range, Body], Range + Body) },
        { "syn": "det(E1) -> 'no'", "sem": lambda: 
            SemanticTemplate([Range, Body], [('none', Range + Body)]) },
        { "syn": "det(E1) -> number(E1)", "sem": lambda number: 
            SemanticTemplate([Range, Body], [('det_equals', Range + Body, number)]) },
        { "syn": "det(E1) -> 'more' 'than' number(E1)", "sem": lambda number: 
            SemanticTemplate([Range, Body], [('det_greater_than', Range + Body, number)]) },

        # superlatives
        { "syn": "superlative(E1) -> 'largest'", "sem": lambda: 
            SemanticTemplate([Body], [('max', E1, E2, Body + [('size_of', E1, E2)])]) },
        { "syn": "superlative(E1) -> 'smallest'", "sem": lambda: 
            SemanticTemplate([Body], [('min', E1, E2, Body + [('size_of', E1, E2)])]) },

        # attribute
        { "syn": "attr(E1, E2) -> 'population'", "sem": lambda: [('has_population', E1, E2)] },
        { "syn": "attr(E1, E2) -> attr(E1, E2) relative_clause(E2)", "sem": lambda attr, relative_clause: attr + relative_clause },

        # number
        { "syn": "number(E1) -> 'one'", "sem": lambda: 1 },
        { "syn": "number(E1) -> 'two'", "sem": lambda: 2 },
        { "syn": "number(E1) -> 'three'", "sem": lambda: 3 },
        { "syn": "number(E1) -> 'four'", "sem": lambda: 4 },
        { "syn": "number(E1) -> 'five'", "sem": lambda: 5 },
        { "syn": "number(E1) -> 'six'", "sem": lambda: 6 },
        { "syn": "number(E1) -> 'seven'", "sem": lambda: 7 },
        { "syn": "number(E1) -> 'eight'", "sem": lambda: 8 },
        { "syn": "number(E1) -> 'nine'", "sem": lambda: 9 },
        { "syn": "number(E1) -> 'ten'", "sem": lambda: 10 },
        { "syn": "number(E1) -> token(E1)", "sem": lambda token: int(token), "if": lambda token: re.match('^\d+$', token) },
        { "syn": "number(E1) -> number(E1) 'million'", "sem": lambda number: number * 1000000 },

        # pp
        { "syn": "pp(E1) -> 'not' pp(E1)", "sem": lambda pp: [('not', pp)] },
        { "syn": "pp(E1) -> 'of' np(E2)", "sem": lambda np: apply(np, [('of', E1, E2)]) },
        { "syn": "pp(E1) -> 'in' np(E2)", "sem": lambda np: apply(np, [('in', E1, E2)]) },
        { "syn": "pp(E1) -> 'south' 'of' np(E2)", "sem": lambda np: apply(np, [('south_of', E1, E2)]) },
        { "syn": "pp(E1) -> pp(E1) 'and' pp(E1)", "sem": lambda pp1, pp2: pp1 + pp2 },

        { "syn": "preposition(E1, E2) -> 'in'", "sem": lambda: [("in", E1, E2)]},
        { "syn": "preposition(E1, E2) -> 'of'", "sem": lambda: [("of", E1, E2)]},

        # adjective phrases
        { "syn": "adjp(E1) -> adj(E1)", "sem": lambda adj: adj },

        { "syn": "adj(E1) -> 'european'", "sem": lambda: [('european', E1)] },
        { "syn": "adj(E1) -> 'african'", "sem": lambda: [('african', E1)] },
        { "syn": "adj(E1) -> 'american'", "sem": lambda: [('american', E1)] },
        { "syn": "adj(E1) -> 'asian'", "sem": lambda: [('asian', E1)] },

        # noun
        { "syn": "noun(E1) -> 'river'", "sem": lambda: [('river', E1)] },
        { "syn": "noun(E1) -> 'rivers'", "sem": lambda: [('river', E1)] },
        { "syn": "noun(E1) -> 'capital'", "sem": lambda: [('capital', E1)] },
        { "syn": "noun(E1) -> 'capitals'", "sem": lambda: [('capital', E1)] },
        { "syn": "noun(E1) -> 'ocean'", "sem": lambda: [('ocean', E1)] },
        { "syn": "noun(E1) -> 'oceans'", "sem": lambda: [('ocean', E1)] },
        { "syn": "noun(E1) -> 'country'", "sem": lambda: [('country', E1)] },
        { "syn": "noun(E1) -> 'countries'", "sem": lambda: [('country', E1)] },
        { "syn": "noun(E1) -> 'sea'", "sem": lambda: [('sea', E1)] },
        { "syn": "noun(E1) -> 'seas'", "sem": lambda: [('sea', E1)] },
        { "syn": "noun(E1) -> 'city'", "sem": lambda: [('city', E1)] },
        { "syn": "noun(E1) -> 'cities'", "sem": lambda: [('city', E1)] },
        { "syn": "noun(E1) -> 'continent'", "sem": lambda: [('continent', E1)] },
        { "syn": "noun(E1) -> 'continents'", "sem": lambda: [('continent', E1)] },
        { "syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },

        # proper noun
        { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token, "inf": [("name", E1)], },
    ]
