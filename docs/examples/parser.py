import os, sys

# Add the directory containing the namespaced modules to sys.path
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + '/../..')

from lib.Pipeline import Pipeline
from lib.entity.SentenceRequest import SentenceRequest
from lib.processor.parser.BasicParser import BasicParser
from lib.processor.tokenizer.BasicTokenizer import BasicTokenizer

def parser_demo():

    grammar = [
        { "syn": "s -> np vp" },
        { "syn": "vp -> verb np" },
        { "syn": "np -> noun" },
        { "syn": "noun -> proper_noun" },
        { "syn": "proper_noun -> 'john'" },
        { "syn": "proper_noun -> 'mary'" },
        { "syn": "verb -> 'loves'" },
    ]

    tokenizer = BasicTokenizer()
    parser = BasicParser(grammar, tokenizer)

    pipeline = Pipeline([
        tokenizer,
        parser
    ])

    request = SentenceRequest("John loves Mary")
    pipeline.enter(request)

    tree = parser.get_tree(request)
    print(tree)

if __name__ == '__main__':
    parser_demo()
