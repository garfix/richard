import unittest

from lib.constants import POS_TYPE_RELATION, POS_TYPE_WORD_FORM
from lib.entity.GrammarRule import GrammarRule
from lib.entity.GrammarRules import GrammarRules
from lib.entity.Log import Log
from lib.entity.RuleConstituent import RuleConstituent
from lib.parser.EarleyParser import EarleyParser

class TestEarleyParser(unittest.TestCase):
   
    def test_upper(self):
        # create a toy grammar to generates superfluous sentences (to test the parsing of ambiguity)
        grammarRules = GrammarRules([
            # s(P1) -> np(E1) vp(P1, E2)
            GrammarRule(
                RuleConstituent("s", ["P1"], POS_TYPE_RELATION),
                [RuleConstituent("np", ["E1"], POS_TYPE_RELATION), RuleConstituent("vp", ["P1", "E2"], POS_TYPE_RELATION)],
                lambda sem: sem
            ),
            # vp(P1, E1) -> verb(P1) np(E1)
            GrammarRule(
                RuleConstituent("vp", ["P1", "E1"], POS_TYPE_RELATION),
                [RuleConstituent("verb", ["P1"], POS_TYPE_RELATION), RuleConstituent("np", ["E1"], POS_TYPE_RELATION)],
                lambda sem: sem
            ),
            # superfluous: s(P1) -> np(E1) verb(P1) np(E2)
            GrammarRule(
                RuleConstituent("s", ["P1"], POS_TYPE_RELATION),
                [RuleConstituent("np", ["E1"], POS_TYPE_RELATION), RuleConstituent("verb", ["P1"], POS_TYPE_RELATION), RuleConstituent("np", ["E2"], POS_TYPE_RELATION)],
                lambda sem: sem
            ),
            # np(E1) -> noun(E1)
            GrammarRule(
                RuleConstituent("np", ["E1"], POS_TYPE_RELATION),
                [RuleConstituent("noun", ["E1"], POS_TYPE_RELATION)],
                lambda sem: sem
            ),
            # noun(E1) -> proper_noun(E1)
            GrammarRule(
                RuleConstituent("noun", ["E1"], POS_TYPE_RELATION),
                [RuleConstituent("proper_noun", ["E1"], POS_TYPE_RELATION)],
                lambda sem: sem
            ),
            # verb(P1) -> "loves"
            GrammarRule(
                RuleConstituent("verb", ["P1"], POS_TYPE_RELATION),
                [RuleConstituent("loves", [], POS_TYPE_WORD_FORM)],
                lambda sem: sem
            ),
            # proper_noun(P1) -> "John"
            GrammarRule(
                RuleConstituent("proper_noun", ["E1"], POS_TYPE_RELATION),
                [RuleConstituent("john", [], POS_TYPE_WORD_FORM)],
                lambda sem: sem
            ),
            # proper_noun(P1) -> "Mary"
            GrammarRule(
                RuleConstituent("proper_noun", ["E1"], POS_TYPE_RELATION),
                [RuleConstituent("mary", [], POS_TYPE_WORD_FORM)],
                lambda sem: sem
            ),            
            # superfluous: noun(P1) -> "John"
            GrammarRule(
                RuleConstituent("noun", ["E1"], POS_TYPE_RELATION),
                [RuleConstituent("john", [], POS_TYPE_WORD_FORM)],
                lambda sem: sem
            ),
        ])
        log = Log(False)
        parser = EarleyParser(log)
        result = parser.parse(grammarRules, ["John", "loves", "Mary"])
        for tree in result.trees:
            print(tree.indented_string("    "))
        self.assertEqual(len(result.trees), 4)
    