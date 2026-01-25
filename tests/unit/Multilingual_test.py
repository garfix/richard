import unittest

from richard.core.BasicSystem import BasicSystem
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.parser.BasicParserProduct import BasicParserProduct
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser

class TestMultilingual(unittest.TestCase):

    def test_two_languages(self):

        grammar_parser = SimpleGrammarRulesParser()

        parser = BasicParser(grammar_parser.parse_read_grammar([
                # English
                { "syn": "s(V) -> np(E1) vp(V, E1)" },
                { "syn": "vp(V, E1) -> verb(V) np(E1)" },
                { "syn": "np(E1) -> noun(E1)" },
                { "syn": "noun(E1) -> proper_noun(E1)" },
                { "syn": "proper_noun(E1) -> 'john'" },
                { "syn": "proper_noun(E1) -> 'mary'" },
                { "syn": "verb(V) -> 'loves'" },
                # Dutch
                { "syn": "s(V) -> np(E1) vp(V, E1)" },
                { "syn": "vp(V, E1) -> verb(V) np(E1)" },
                { "syn": "np(E1) -> noun(E1)" },
                { "syn": "noun(E1) -> proper_noun(E1)" },
                { "syn": "proper_noun(E1) -> 'jan'" },
                { "syn": "proper_noun(E1) -> 'marie'" },
                { "syn": "verb(V) -> 'houdt' 'van'" },
            ]))

        system = BasicSystem(
            parser=parser
        )

        request = SentenceRequest("John loves Mary")

        response: BasicParserProduct = system.enter(request)
        self.assertEqual(response.products[0].parse_trees[0].inline_str(), "s(np(noun(proper_noun(john 'john'))) vp(verb(loves 'loves') np(noun(proper_noun(mary 'mary')))))")

        request = SentenceRequest("Jan houdt van Marie")

        response: BasicParserProduct = system.enter(request)
        self.assertEqual(response.products[0].parse_trees[0].inline_str(), "s(np(noun(proper_noun(jan 'jan'))) vp(verb(houdt 'houdt' van 'van') np(noun(proper_noun(marie 'marie')))))")
