import unittest

from richard.core.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.entity.ParseTreeNode import ParseTreeNode
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.language_selector.LanguageSelector import LanguageSelector
from richard.processor.language_selector.Multilingual import Multilingual
from richard.processor.parser.BasicParserProduct import BasicParserProduct
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer

class TestMultilingual(unittest.TestCase):

    def test_two_languages(self):

        language_selector = LanguageSelector(["en_US", "nl_NL"])
        tokenizer = BasicTokenizer()

        parsers = {
            "nl_NL": BasicParser([
                { "syn": "s(V) -> np(E1) vp(V, E1)" },
                { "syn": "vp(V, E1) -> verb(V) np(E1)" },
                { "syn": "np(E1) -> noun(E1)" },
                { "syn": "noun(E1) -> proper_noun(E1)" },
                { "syn": "proper_noun(E1) -> 'john'" },
                { "syn": "proper_noun(E1) -> 'mary'" },
                { "syn": "verb(V) -> 'loves'" },
            ], tokenizer),
            "en_US": BasicParser([
                { "syn": "s(V) -> np(E1) vp(V, E1)" },
                { "syn": "vp(V, E1) -> verb(V) np(E1)" },
                { "syn": "np(E1) -> noun(E1)" },
                { "syn": "noun(E1) -> proper_noun(E1)" },
                { "syn": "proper_noun(E1) -> 'jan'" },
                { "syn": "proper_noun(E1) -> 'marie'" },
                { "syn": "verb(V) -> 'houdt' 'van'" },
            ], tokenizer)
        }

        parser = Multilingual(parsers, language_selector)

        pipeline = Pipeline([
            FindOne(language_selector),
            FindOne(tokenizer),
            FindOne(parser)
        ])

        request = SentenceRequest("John loves Mary")

        parse_tree: ParseTreeNode = pipeline.enter(request)
        self.assertEqual(parse_tree.inline_str(), "s(np(noun(proper_noun(john 'John'))) vp(verb(loves 'loves') np(noun(proper_noun(mary 'Mary')))))")

        request = SentenceRequest("Jan houdt van Marie")

        parse_tree: ParseTreeNode = pipeline.enter(request)
        self.assertEqual(parse_tree.inline_str(), "s(np(noun(proper_noun(jan 'Jan'))) vp(verb(houdt 'houdt' van 'van') np(noun(proper_noun(marie 'Marie')))))")
