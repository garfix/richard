import re
from lib.constants import POS_TYPE_RELATION, POS_TYPE_WORD_FORM
from lib.entity.GrammarRule import GrammarRule
from lib.entity.GrammarRules import GrammarRules
from lib.entity.SentenceRequest import SentenceRequest
from lib.entity.RuleConstituent import RuleConstituent
from lib.interface.Processor import Processor
from lib.type.SimpleGrammar import SimpleGrammar
from .EarleyParser import EarleyParser


class BasicParser(Processor):

    tokenizer: Processor
    grammar_rules: GrammarRules
    parser: EarleyParser

    re_rule: re.Pattern
    re_space: re.Pattern


    def __init__(self, grammar: SimpleGrammar, tokenizer: Processor) -> None:

        self.tokenizer = tokenizer

        self.re_rule = re.compile("\s*(\w+)\s*->((\s*[\w']+)+)")
        self.re_space = re.compile("\s+")

        self.grammar_rules = self.parse_simple_grammar_rules(grammar)
        self.parser = EarleyParser()


    def parse_simple_grammar_rules(self, simple_grammar: SimpleGrammar):

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

            rules.append(GrammarRule(antecedent, consequents, lambda sem: sem))

        return GrammarRules(rules)
            

    def process(self, request: SentenceRequest):
        tokens = request.get_current_product(self.tokenizer)
        result = self.parser.parse(self.grammar_rules, tokens)
        return result.trees
    
