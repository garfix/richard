from richard.core.constants import E1, E2, E3, E4, e1, e2, e3, Body, Range
from richard.processor.parser.helper.grammar_functions import apply
from richard.type.SemanticTemplate import SemanticTemplate



def get_grammar2():
    return [

        # sentence
        {
            "syn": "s(E1) -> np(E2) vp(E2)",
            "sem": lambda np, vp: [('knows', apply(np, vp), E1)],
            "inf": [("format", "y/n/u"), ("format_ynu", e1)],
        },

        # vp
        { "syn": "vp(E1) -> is(E3) np(E2)", "sem": lambda is1, np: apply(np, [('isa', E1, E2)]) },
        { "syn": "vp(E1) -> is(E3) 'not' np(E2)", "sem": lambda is1, np: apply(np, [('negate', [('isa', E1, E2)])]) },

        # copula
        { "syn": "is(E1) -> 'is'", "sem": lambda: [] },

        # article
        { "syn": "a(E1) -> 'a'", "sem": lambda: [] },
        { "syn": "a(E1) -> 'an'", "sem": lambda: [] },

        # np
        { "syn": "np(E1) -> nbar(E1)", "sem": lambda nbar:
            SemanticTemplate([Body], nbar + Body) },
        { "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar:
            SemanticTemplate([Body], apply(det, nbar, Body)) },

        # det
        { "syn": "det(E1) -> 'a'", "sem": lambda:
            SemanticTemplate([Range, Body], Range + Body) },

        # nbar
        { "syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun },

        # noun
        { "syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },


        # proper noun
        { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },


        # noun
        # { "syn": "noun(E1) -> 'magnesium'", "sem": lambda: [('magnesium', E1)] },
        # { "syn": "noun(E1) -> 'magnesium' 'oxide'", "sem": lambda: [('magnesium_oxide', E1)] },
        # { "syn": "noun(E1) -> 'oxygen'", "sem": lambda: [('oxygen', E1)] },
        # { "syn": "noun(E1) -> 'iron'", "sem": lambda: [('iron', E1)] },
        # { "syn": "noun(E1) -> 'sulfur'", "sem": lambda: [('sulfur', E1)] },
        # { "syn": "noun(E1) -> 'nitrogen'", "sem": lambda: [('nitrogen', E1)] },
        # { "syn": "noun(E1) -> 'hydrogen'", "sem": lambda: [('hydrogen', E1)] },
        # { "syn": "noun(E1) -> 'carbon'", "sem": lambda: [('carbon', E1)] },
        # { "syn": "noun(E1) -> 'copper'", "sem": lambda: [('copper', E1)] },
        # { "syn": "noun(E1) -> 'metals'", "sem": lambda: [('metal', E1)] },
        # { "syn": "noun(E1) -> 'nonmetal'", "sem": lambda: [('nonmetal', E1)] },
        # { "syn": "noun(E1) -> 'thing'", "sem": lambda: [('thing', E1)] },
        # { "syn": "noun(E1) -> 'things'", "sem": lambda: [('thing', E1)] },
        # { "syn": "noun(E1) -> 'solid'", "sem": lambda: [('solid', E1)] },

        # { "syn": "noun(E1) -> 'gasoline'", "sem": lambda: [('gasoline', E1)] },
        # { "syn": "noun(E1) -> 'fuels'", "sem": lambda: [('fuel', E1)] },
        # { "syn": "noun(E1) -> 'ice'", "sem": lambda: [('ice', E1)] },
        # { "syn": "noun(E1) -> 'steam'", "sem": lambda: [('steam', E1)] },

        # { "syn": "noun(E1) -> 'sugar'", "sem": lambda: [('sugar', E1)] },
        # { "syn": "noun(E1) -> 'water'", "sem": lambda: [('water', E1)] },
        # { "syn": "noun(E1) -> 'sulfuric' 'acid'", "sem": lambda: [('sulfuric_acid', E1)] },
        # { "syn": "noun(E1) -> 'sodium' 'chloride'", "sem": lambda: [('sodium_chloride', E1)] },
        # { "syn": "noun(E1) -> 'ferrous sulfide'", "sem": lambda: [('ferrous_sulfide', E1)] },
        # { "syn": "noun(E1) -> 'oxide'", "sem": lambda: [('oxide', E1)] },
        # { "syn": "noun(E1) -> 'oxides'", "sem": lambda: [('oxides', E1)] },
        # { "syn": "noun(E1) -> 'salt'", "sem": lambda: [('salt', E1)] },

        # { "syn": "noun(E1) -> 'elements'", "sem": lambda: [('element', E1)] },
        # { "syn": "noun(E1) -> 'compound'", "sem": lambda: [('compound', E1)] },
    ]
