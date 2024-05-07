import unittest

from lib.Pipeline import Pipeline
from lib.entity.SentenceRequest import SentenceRequest
from lib.processor.language_selector.LanguageSelector import LanguageSelector
from lib.processor.language_selector.MultiLingual import MultiLingual
from lib.processor.parser.BasicParser import BasicParser
from lib.processor.tokenizer.BasicTokenizer import BasicTokenizer

class TestMultilingual(unittest.TestCase):
   
    def test_two_languages(self):

        language_selector = LanguageSelector(["en_US", "nl_NL"])
        tokenizer = BasicTokenizer()

        parsers = {
        "nl_NL": BasicParser([
            { "syn": "s -> np vp" },
            { "syn": "vp -> verb np" },
            { "syn": "np -> noun" },
            { "syn": "noun -> proper_noun" },
            { "syn": "proper_noun -> 'john'" },
            { "syn": "proper_noun -> 'mary'" },
            { "syn": "verb -> 'loves'" },
        ], tokenizer),

        "en_US": BasicParser([
            { "syn": "s -> np vp" },
            { "syn": "vp -> verb np" },
            { "syn": "np -> noun" },
            { "syn": "noun -> proper_noun" },
            { "syn": "proper_noun -> 'jan'" },
            { "syn": "proper_noun -> 'marie'" },
            { "syn": "verb -> 'houdt' 'van'" },
        ], tokenizer)}

        parser = MultiLingual(parsers, language_selector)

        pipeline = Pipeline([
            language_selector,
            tokenizer,
            parser
        ])

        request = SentenceRequest("John loves Mary")

        pipeline.enter(request)

        tree = request.get_current_product(parser)

        print(tree)

        request = SentenceRequest("Jan houdt van Marie")

        pipeline.enter(request)

        tree = request.get_current_product(parser)

        print(tree)
        