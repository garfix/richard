import re

from richard.constants import POS_TYPE_RELATION, POS_TYPE_WORD_FORM
from richard.entity.GrammarRule import GrammarRule
from richard.entity.GrammarRules import GrammarRules
from richard.entity.RuleConstituent import RuleConstituent
from richard.entity.Variable import Variable
from richard.type.InferenceRule import InferenceRule
from richard.type.SimpleGrammar import SimpleGrammar


class SimpleInferenceRuleParser:
    re_tokens: re.Pattern
    re_comma: re.Pattern
    re_atom: re.Pattern


    def __init__(self) -> None:
        self.re_tokens = re.compile("(?:\.|,\w*|:-|'(?:\\\\'|[^'])+'|\w[^\)]+\))")
        self.re_comma = re.compile("\s*,\s*")
        self.re_atom = re.compile('([^\(]+)\(([^\)]+)\)')


    def parse(self, text: str):

        tokens = re.findall(self.re_tokens, text)

        if not tokens:
            raise Exception("Could not parse rule or fact: " + text)
        
        if tokens[-1] != ".":
            raise Exception("An inference rule or fact should end with a dot: " + text)

        if len(tokens) == 2:
            antecedent = self.parse_atom(tokens[0])
            consequents = []
        else:         
            if tokens[1] != ':-':
                raise Exception("Missing :- operator in rule: " + text)
        
            antecedent = self.parse_atom(tokens[0])
            if not antecedent:
                raise Exception("Could not parse antecedent: " + text)

            consequents = []
            for i, raw_consequent in enumerate(tokens[2:-1]):
                if i > 0 and i % 2 == 1:
                    if raw_consequent.strip() != ",":
                        raise Exception("Missing comma in rule: " + text)
                    continue

                consequent = self.parse_atom(raw_consequent)
                if not consequent:
                    raise Exception("Could not parse consequent: " + raw_consequent)
                consequents.append(consequent)

        return InferenceRule(antecedent, consequents)
    

    def parse_atom(self, token: str):
        result = re.fullmatch(self.re_atom, token)
        if not result:
            return False
        predicate = result[1]
        variables = re.split(self.re_comma, result[2])        
        return tuple([predicate] + [Variable(v) for v in variables])
    