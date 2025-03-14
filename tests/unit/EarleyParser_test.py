import unittest

from richard.core.constants import POS_TYPE_RELATION, POS_TYPE_WORD_FORM
from richard.entity.GrammarRule import GrammarRule
from richard.entity.GrammarRules import GrammarRules
from richard.entity.RuleConstituent import RuleConstituent
from richard.processor.parser.earley.EarleyParser import EarleyParser

class TestEarleyParser(unittest.TestCase):

    def test_ambiguity(self):
        # create a toy grammar to generates superfluous sentences (to test the parsing of ambiguity)
        grammarRules = GrammarRules([
            # s(P1) -> np(E1) vp(P1, E2)
            GrammarRule(
                RuleConstituent("s", ["P1"], POS_TYPE_RELATION),
                [
                    RuleConstituent("np", ["E1"], POS_TYPE_RELATION),
                    RuleConstituent(" ", [], POS_TYPE_WORD_FORM),
                    RuleConstituent("vp", ["P1", "E2"], POS_TYPE_RELATION)
                ],
            ),
            # vp(P1, E1) -> verb(P1) np(E1)
            GrammarRule(
                RuleConstituent("vp", ["P1", "E1"], POS_TYPE_RELATION),
                [
                    RuleConstituent("verb", ["P1"], POS_TYPE_RELATION),
                    RuleConstituent(" ", [], POS_TYPE_WORD_FORM),
                    RuleConstituent("np", ["E1"], POS_TYPE_RELATION)
                ],
            ),
            # superfluous: s(P1) -> np(E1) verb(P1) np(E2)
            GrammarRule(
                RuleConstituent("s", ["P1"], POS_TYPE_RELATION),
                [
                    RuleConstituent("np", ["E1"], POS_TYPE_RELATION),
                    RuleConstituent(" ", [], POS_TYPE_WORD_FORM),
                    RuleConstituent("verb", ["P1"], POS_TYPE_RELATION),
                    RuleConstituent(" ", [], POS_TYPE_WORD_FORM),
                    RuleConstituent("np", ["E2"], POS_TYPE_RELATION)
                ],
            ),
            # np(E1) -> noun(E1)
            GrammarRule(
                RuleConstituent("np", ["E1"], POS_TYPE_RELATION),
                [RuleConstituent("noun", ["E1"], POS_TYPE_RELATION)],
            ),
            # noun(E1) -> proper_noun(E1)
            GrammarRule(
                RuleConstituent("noun", ["E1"], POS_TYPE_RELATION),
                [RuleConstituent("proper_noun", ["E1"], POS_TYPE_RELATION)],
            ),
            # verb(P1) -> "loves"
            GrammarRule(
                RuleConstituent("verb", ["P1"], POS_TYPE_RELATION),
                [RuleConstituent("loves", [], POS_TYPE_WORD_FORM)],
            ),
            # proper_noun(P1) -> "John"
            GrammarRule(
                RuleConstituent("proper_noun", ["E1"], POS_TYPE_RELATION),
                [RuleConstituent("john", [], POS_TYPE_WORD_FORM)],
            ),
            # proper_noun(P1) -> "Mary"
            GrammarRule(
                RuleConstituent("proper_noun", ["E1"], POS_TYPE_RELATION),
                [RuleConstituent("mary", [], POS_TYPE_WORD_FORM)],
            ),
            # superfluous: noun(P1) -> "John"
            GrammarRule(
                RuleConstituent("noun", ["E1"], POS_TYPE_RELATION),
                [RuleConstituent("john", [], POS_TYPE_WORD_FORM)],
            ),
        ])
        parser = EarleyParser()
        result = parser.parse(grammarRules, "John loves Mary")

        self.assertEqual(len(result.products), 4)
        self.assertEqual(result.products[0].inline_str(), "s(np(noun(john 'john')) verb(loves 'loves') np(noun(proper_noun(mary 'mary'))))")
        self.assertEqual(result.products[1].inline_str(), "s(np(noun(proper_noun(john 'john'))) verb(loves 'loves') np(noun(proper_noun(mary 'mary'))))")
        self.assertEqual(result.products[2].inline_str(), "s(np(noun(john 'john')) vp(verb(loves 'loves') np(noun(proper_noun(mary 'mary')))))")
        self.assertEqual(result.products[3].inline_str(), "s(np(noun(proper_noun(john 'john'))) vp(verb(loves 'loves') np(noun(proper_noun(mary 'mary')))))")

