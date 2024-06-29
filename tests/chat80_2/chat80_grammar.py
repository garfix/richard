from richard.Model import Model
from richard.constants import E1, E2, EXISTS


def get_grammar(model: Model):
    return [

        # sentence
        { "syn": "s(E1) -> 'what' nbar(E1) 'are' 'there' '?'", "sem": lambda nbar: nbar },
        { "syn": "s(E1) -> 'does' np(E1) vp_nosub_obj(E1) '?'",  "sem": lambda np, vp_nosub_obj: [('check', E1, np, vp_nosub_obj)] },
        { "syn": "s(E1) -> 'what' 'is' np(E1) '?'", "sem": lambda np: [('check', E1, np, [])] },

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

        # det
        { "syn": "det(E1) -> 'the'", "sem": lambda: EXISTS },

        # pp
        { "syn": "pp(E1) -> 'of' np(E2)", "sem": lambda np: [('check', E2, np, [('of', E1, E2)])] },

        # noun
        { "syn": "noun(E1) -> 'rivers'", "sem": lambda: [('river', E1)] },
        { "syn": "noun(E1) -> 'capital'", "sem": lambda: [('capital', E1)] },
        { "syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },
        { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },
    ]
