from richard.Model import Model
from richard.entity.Instance import Instance
from richard.entity.Variable import Variable
from richard.module.CoreModule import EXISTS


E1 = Variable('E1')
E2 = Variable('E2')

def get_grammar(model: Model):
    return [

        # sentences
        { "syn": "s(E1) -> 'what' nbar(E1) 'are' 'there' '?'", "sem": lambda nbar: nbar },
        { "syn": "s(E1) -> 'does' np(E1) vp_nosub_obj(E1) '?'",  "sem": lambda np, vp_nosub_obj: [('check', E1, np, vp_nosub_obj)] },

        # active transitive: sub obj
        { "syn": "vp_nosub_obj(E1) -> vp_nosub_noobj(E1, E2) np(E2)", "sem": lambda vp_nosub_noobj, np: [('check', E2, np, vp_nosub_noobj)] },
        { "syn": "vp_nosub_obj(E1) -> 'does' 'not' vp_nosub_noobj(E1, E2) np(E2)", "sem": lambda vp_nosub_noobj, np: [('check', E2, np, vp_nosub_noobj)] },
        { "syn": "vp_nosub_noobj(E1, E2) -> tv(E1, E2)", "sem": lambda tv: tv },

        { "syn": "tv(E1, E2) -> 'border'", "sem": lambda: [('borders', E1, E2)] },

        # nps
        { "syn": "np(E1) -> nbar(E1)", "sem": lambda nbar: ('quant', E1, EXISTS, nbar) },

        # nbars
        { "syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun },

        # nouns
        { "syn": "noun(E1) -> 'rivers'", "sem": lambda: [('river', E1)] },
        { "syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },
        { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },
    ]
