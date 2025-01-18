import unittest

from richard.core.Pipeline import Pipeline
from richard.block.FindOne import FindOne
from richard.entity.ParseTreeNode import ParseTreeNode
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.language_selector.LanguageSelector import LanguageSelector
from richard.processor.language_selector.Multilingual import Multilingual
from richard.processor.parser.BasicParserProduct import BasicParserProduct
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser

class TestMultilingual(unittest.TestCase):

    def test_two_languages(self):

        language_selector = LanguageSelector(["en_US", "nl_NL"])
        grammar_parser = SimpleGrammarRulesParser()

        parsers = {
            "nl_NL": BasicParser(grammar_parser.parse_read_grammar([
                { "syn": "s(V) -> np(E1) vp(V, E1)" },
                { "syn": "vp(V, E1) -> verb(V) np(E1)" },
                { "syn": "np(E1) -> noun(E1)" },
                { "syn": "noun(E1) -> proper_noun(E1)" },
                { "syn": "proper_noun(E1) -> 'john'" },
                { "syn": "proper_noun(E1) -> 'mary'" },
                { "syn": "verb(V) -> 'loves'" },
            ])),
            "en_US": BasicParser(grammar_parser.parse_read_grammar([
                { "syn": "s(V) -> np(E1) vp(V, E1)" },
                { "syn": "vp(V, E1) -> verb(V) np(E1)" },
                { "syn": "np(E1) -> noun(E1)" },
                { "syn": "noun(E1) -> proper_noun(E1)" },
                { "syn": "proper_noun(E1) -> 'jan'" },
                { "syn": "proper_noun(E1) -> 'marie'" },
                { "syn": "verb(V) -> 'houdt' 'van'" },
            ]))
        }

        parser = Multilingual(parsers, language_selector)

        pipeline = Pipeline([
            FindOne(language_selector),
            FindOne(parser)
        ])

        request = SentenceRequest("John loves Mary")

        parse_tree: ParseTreeNode = pipeline.enter(request)
        self.assertEqual(parse_tree.inline_str(), "s(np(noun(proper_noun(john 'john'))) vp(verb(loves 'loves') np(noun(proper_noun(mary 'mary')))))")

        request = SentenceRequest("Jan houdt van Marie")

        parse_tree: ParseTreeNode = pipeline.enter(request)
        self.assertEqual(parse_tree.inline_str(), "s(np(noun(proper_noun(jan 'jan'))) vp(verb(houdt 'houdt' van 'van') np(noun(proper_noun(marie 'marie')))))")
