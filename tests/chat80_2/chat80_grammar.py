from richard.Model import Model
from richard.constants import E1, E2, E3, EXISTS


def get_grammar(model: Model):
    return [

        # sentence
        { "syn": "s(E1) -> 'what' nbar(E1) 'are' 'there' '?'", "sem": lambda nbar: nbar, 
            "intents": ["what"] },
        { "syn": "s(E1) -> 'does' np(E1) vp_nosub_obj(E1) '?'",  "sem": lambda np, vp_nosub_obj: [('check', E1, np, vp_nosub_obj)], 
            "intents": ["y/n"] },
        { "syn": "s(E1) -> 'what' 'is' np(E1) '?'", "sem": lambda np: [('check', E1, np, [])], 
            "intents": ["what"] },
        { "syn": "s(E2) -> 'where' 'is' np(E1) '?'", "sem": lambda np: [('check', E1, np, []), ('where', E1, E2)], 
            "intents": ["where"] },
        { "syn": "s(E1) -> 'which' nbar(E1) 'are' adjp(E1) '?'", "sem": lambda nbar, adjp: nbar + adjp, 
            "intents": ["which"] },
        { "syn": "s(E1) -> 'which' nbar(E1) '\\'' 's' np(E2) 'is' np(E3) '?'", "sem": lambda nbar, np1, np2: 
         nbar + [('check', E2, np1, [('of', E2, E1), ('check', E3, np2, [('==', E2, E3)])])],
             "intents": ["which"] },

        # active transitive: sub obj
        { "syn": "vp_nosub_obj(E1) -> vp_nosub_noobj(E1, E2) np(E2)", "sem": lambda vp_nosub_noobj, np: [('check', E2, np, vp_nosub_noobj)] },
        { "syn": "vp_nosub_obj(E1) -> 'does' 'not' vp_nosub_noobj(E1, E2) np(E2)", "sem": lambda vp_nosub_noobj, np: [('check', E2, np, vp_nosub_noobj)] },
        { "syn": "vp_nosub_noobj(E1, E2) -> tv(E1, E2)", "sem": lambda tv: tv },

        { "syn": "tv(E1, E2) -> 'border'", "sem": lambda: [('borders', E1, E2)] },

        # np
        { "syn": "np(E1) -> nbar(E1)", "sem": lambda nbar: ('quant', E1, EXISTS, nbar) },
        { "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar: ('quant', E1, det, nbar) },

        # nbar
        { "syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun },
        { "syn": "nbar(E1) -> nbar(E1) pp(E1)", "sem": lambda nbar, pp: nbar + pp },
        { "syn": "nbar(E1) -> superlative(E1, E2) nbar(E1)", "sem": lambda superlative, nbar: [('aggregate', nbar, superlative, E1)] },

        # det
        { "syn": "det(E1) -> 'the'", "sem": lambda: EXISTS },

        # pp
        { "syn": "pp(E1) -> 'of' np(E2)", "sem": lambda np: [('check', E2, np, [('of', E1, E2)])] },

        # adjective phrases
        { "syn": "adjp(E1) -> adj(E1)", "sem": lambda adj: adj },

        { "syn": "adj(E1) -> 'european'", "sem": lambda: [('european', E1)] },
        { "syn": "adj(E1) -> 'african'", "sem": lambda: [('african', E1)] },
        { "syn": "adj(E1) -> 'american'", "sem": lambda: [('american', E1)] },
        { "syn": "adj(E1) -> 'asian'", "sem": lambda: [('asian', E1)] },

        # superlatives
        { "syn": "superlative(E1, E2) -> 'largest'", "sem": lambda: ('aggregation', E1, E2, [('size-of', E1, E2)], 'max') },
        { "syn": "superlative(E1, E2) -> 'smallest'", "sem": lambda: ('aggregation', E1, E2, [('size-of', E1, E2)], 'min') },

        # noun
        { "syn": "noun(E1) -> 'rivers'", "sem": lambda: [('river', E1)] },
        { "syn": "noun(E1) -> 'capital'", "sem": lambda: [('capital', E1)] },
        { "syn": "noun(E1) -> 'country'", "sem": lambda: [('country', E1)] },
        { "syn": "noun(E1) -> 'countries'", "sem": lambda: [('country', E1)] },
        { "syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },

        # proper noun
        { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },
    ]
