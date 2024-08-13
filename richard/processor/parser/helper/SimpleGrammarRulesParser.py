import re

from richard.constants import POS_TYPE_RELATION, POS_TYPE_WORD_FORM
from richard.entity.GrammarRule import GrammarRule
from richard.entity.GrammarRules import GrammarRules
from richard.entity.RuleConstituent import RuleConstituent
from richard.entity.Variable import Variable
from richard.type.SimpleGrammar import SimpleGrammar


class SimpleGrammarRulesParser:
    re_tokens: re.Pattern
    re_comma: re.Pattern
    re_atom: re.Pattern


    def __init__(self) -> None:
        self.re_tokens = re.compile("(?:->|'(?:\\\\'|[^'])+'|\w[^\)]+\))")
        self.re_comma = re.compile("\s*,\s*")
        self.re_atom = re.compile('([^\(]+)\(([^\)]+)\)')


    def parse(self, simple_grammar: SimpleGrammar):
        rules = []

        for simple_rule in simple_grammar:
            if not 'syn' in simple_rule:
                raise Exception("A rule must contain a 'syn' value")
            syntax = simple_rule['syn']

            tokens = re.findall(self.re_tokens, syntax)
            if len(tokens) < 3:
                raise Exception("Could not parse 'syn' value: " + syntax)            
            
            if tokens[1] != '->':
                raise Exception("Missing -> operator in 'syn' value: " + syntax)
            
            antecedent = self.parse_atom(tokens[0])
            if not antecedent:
                raise Exception("Could not parse antecedent: " + syntax)

            consequents = []
            for raw_consequent in tokens[2:]:
                if raw_consequent[0] == "'":
                    raw_consequent = raw_consequent[1:-1]
                    raw_consequent = raw_consequent.replace("\\'", "'")
                    consequents.append(RuleConstituent(raw_consequent, [], POS_TYPE_WORD_FORM))
                else:
                    consequent = self.parse_atom(raw_consequent)
                    if not consequent:
                        raise Exception("Could not parse consequent: " + syntax)
                    consequents.append(consequent)

            sem = None
            if 'sem' in simple_rule:
                sem = simple_rule['sem']

            inferences = []
            if 'inf' in simple_rule:
                inferences = simple_rule['inf']

            intents = []
            if 'intents' in simple_rule:
                intents = simple_rule['intents']

            condition = None
            if 'if' in simple_rule:
                condition = simple_rule['if']

            boost = 0
            if 'boost' in simple_rule:
                boost = simple_rule['boost']
            rules.append(GrammarRule(antecedent, consequents, sem=sem, inferences=inferences, intents=intents, boost=boost, condition=condition))

        return GrammarRules(rules)
    

    def parse_atom(self, token: str):
        result = re.fullmatch(self.re_atom, token)
        if not result:
            return False
        predicate = result[1]
        variables = re.split(self.re_comma, result[2])        
        return RuleConstituent(predicate, variables, POS_TYPE_RELATION)
    