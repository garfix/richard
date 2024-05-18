import unittest

from richard.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.language_selector.LanguageSelector import LanguageSelector
from richard.processor.language_selector.Multilingual import Multilingual
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer

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
            ], tokenizer)
        }

        parser = Multilingual(parsers, language_selector)

        pipeline = Pipeline([
            FindOne(language_selector),
            FindOne(tokenizer),
            FindOne(parser)
        ])

        request = SentenceRequest("John loves Mary")

        pipeline.enter(request)
        tree = parser.get_product(request)
        self.assertEqual(tree.inline_str(), "s(np(noun(proper_noun(john 'John'))) vp(verb(loves 'loves') np(noun(proper_noun(mary 'Mary')))))")

        request = SentenceRequest("Jan houdt van Marie")

        pipeline.enter(request)
        tree = parser.get_product(request)
        self.assertEqual(tree.inline_str(), "s(np(noun(proper_noun(jan 'Jan'))) vp(verb(houdt 'houdt' van 'van') np(noun(proper_noun(marie 'Marie')))))")
        