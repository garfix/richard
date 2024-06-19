from richard.Model import Model
from richard.entity.Variable import Variable

E1 = Variable('E1')
E2 = Variable('E2')

def get_grammar(model: Model):
    return [

        # sentences
        { "syn": "s -> 'what' nbar 'are' 'there' '?'", "sem": lambda nbar: lambda: nbar },

        # nbars
        { "syn": "nbar -> noun", "sem": lambda noun: noun },

        # nouns
        { "syn": "noun -> 'rivers'", "sem": lambda: (('river', E1)) },

    ]
