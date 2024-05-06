import unittest

from lib.Pipeline import Pipeline
from lib.entity.SentenceRequest import SentenceRequest
from lib.processor.language_switcher.LanguageSwitcher import LanguageSwitcher
from lib.processor.parser.MultiLingualParser import MultiLingualParser
from lib.processor.tokenizer.BasicTokenizer import BasicTokenizer

class TestMultilingual(unittest.TestCase):
   
    def test_two_languages(self):

        grammars = {
        "nl_NL": [
            { "syn": "s -> np vp" },
            { "syn": "vp -> verb np" },
            { "syn": "np -> noun" },
            { "syn": "noun -> proper_noun" },
            { "syn": "proper_noun -> 'john'" },
            { "syn": "proper_noun -> 'mary'" },
            { "syn": "verb -> 'loves'" },
        ],

        "en_US": [
            { "syn": "s -> np vp" },
            { "syn": "vp -> verb np" },
            { "syn": "np -> noun" },
            { "syn": "noun -> proper_noun" },
            { "syn": "proper_noun -> 'jan'" },
            { "syn": "proper_noun -> 'marie'" },
            { "syn": "verb -> 'belieft'" },
        ]}

        language_switcher = LanguageSwitcher(["en_US", "nl_NL"])
        tokenizer = BasicTokenizer()
        parser = MultiLingualParser(grammars, language_switcher, tokenizer)

        pipeline = Pipeline([
            language_switcher,
            tokenizer,
            parser
        ])

        request = SentenceRequest("John loves Mary")

        pipeline.enter(request)

        tree = request.get_current_product(parser)

        print(tree)

        request = SentenceRequest("Jan belieft Marie")

        pipeline.enter(request)

        tree = request.get_current_product(parser)

        print(tree)
        