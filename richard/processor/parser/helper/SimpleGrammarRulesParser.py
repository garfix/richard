import re

from richard.constants import POS_TYPE_RELATION, POS_TYPE_WORD_FORM
from richard.entity.GrammarRule import GrammarRule
from richard.entity.GrammarRules import GrammarRules
from richard.entity.RuleConstituent import RuleConstituent
from richard.type.SimpleGrammar import SimpleGrammar


class SimpleGrammarRulesParser:
    re_rule: re.Pattern
    re_space: re.Pattern


    def __init__(self) -> None:
        self.re_rule = re.compile("\s*(\w+)\s*->((\s*[\S]+)+)")
        self.re_space = re.compile("\s+")


    def parse(self, simple_grammar: SimpleGrammar):
        rules = []

        for simple_rule in simple_grammar:
            if not 'syn' in simple_rule:
                raise Exception("A rule must contain a 'syn' value")
            syntax = simple_rule['syn']

            result = self.re_rule.match(syntax)
            if not result:
                raise Exception("Could not parse 'syn' value: " + syntax)            
            
            simple_antecedent = result.group(1)
            simple_consequents = re.split(self.re_space, result.group(2).strip())

            antecedent = RuleConstituent(simple_antecedent, ["X"], POS_TYPE_RELATION)
            consequents = []
            for simple_consequent in simple_consequents:
                if simple_consequent[0] == "'":
                    simple_consequent = simple_consequent[1:-1]
                    consequents.append(RuleConstituent(simple_consequent, [], POS_TYPE_WORD_FORM))
                else:
                    consequents.append(RuleConstituent(simple_consequent, ["X"], POS_TYPE_RELATION))

            sem = None
            if 'sem' in simple_rule:
                sem = simple_rule['sem']
            rules.append(GrammarRule(antecedent, consequents, sem))

        return GrammarRules(rules)
    