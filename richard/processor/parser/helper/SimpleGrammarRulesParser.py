import re

from build.lib.richard.type import SimpleGrammarRule
from richard.core.constants import POS_TYPE_REG_EXP, POS_TYPE_RELATION, POS_TYPE_WORD_FORM
from richard.entity.GrammarRule import GrammarRule
from richard.entity.GrammarRules import GrammarRules
from richard.entity.RuleConstituent import RuleConstituent
from richard.entity.Variable import Variable
from richard.type.SimpleGrammar import SimpleGrammar


class SimpleGrammarRulesParser:
    re_tokens: re.Pattern
    re_identifier: re.Pattern
    re_variable: re.Pattern


    def __init__(self) -> None:
        self.re_tokens = re.compile("(" + "|".join([
            ',',
            '->',
            '\(',
            '\)',
            "/(?:\\\\/|[^/])+/",
            "'(?:\\\\'|[^'])+'",
            '"(?:\\\\"|[^"])+"',
            '[A-Z]\w*',
            '\w+',
            '\\+',
            '~',
        ]) + ")")
        self.re_identifier = re.compile("^\w+$")
        self.re_variable = re.compile("^[A-Z]\w*$")


    def parse(self, simple_grammar: SimpleGrammar) -> GrammarRules:
        rules = []

        for simple_rule in simple_grammar:
            rule = self.parse_simple_rule(simple_rule)
            rules.append(rule)

        return GrammarRules(rules)


    def parse_simple_rule(self, simple_rule: SimpleGrammarRule) -> GrammarRule:
        if not 'syn' in simple_rule:
            raise Exception("A rule must contain a 'syn' value")

        antecedent, consequents = self.parse_syntax(simple_rule['syn'])

        sem = None
        if 'sem' in simple_rule:
            sem = simple_rule['sem']

        exec = None
        if 'exec' in simple_rule:
            exec = simple_rule['exec']

        inferences = []
        if 'inf' in simple_rule:
            inferences = simple_rule['inf']

        boost = 0
        if 'boost' in simple_rule:
            boost = simple_rule['boost']

        return GrammarRule(antecedent, consequents, sem=sem, exec=exec, inferences=inferences, boost=boost)


    def parse_syntax(self, syntax):

        tokens = re.findall(self.re_tokens, syntax)

        pos = 0
        antecedent, new_pos = self.parse_atom(tokens, pos)
        if not antecedent:
            raise Exception("Could not parse antecedent: " + syntax)
        pos = new_pos

        token, new_pos = self.parse_token(tokens, pos)
        if token != "->":
            raise Exception("Missing -> operator in 'syn' value: " + syntax)
        pos = new_pos

        consequents = []
        while True:

            atom, new_pos = self.parse_atom(tokens, pos)
            if atom:
                consequents.append(atom)
            else:

                regexp, new_pos = self.parse_regexp(tokens, pos)
                if regexp:
                    atom = RuleConstituent(regexp, [], POS_TYPE_REG_EXP)
                    consequents.append(atom)
                else:

                    string, new_pos = self.parse_string(tokens, pos)
                    if not string:
                        break

                    atom = RuleConstituent(string, [], POS_TYPE_WORD_FORM)
                    consequents.append(atom)

            pos = new_pos

            token, new_pos = self.parse_token(tokens, pos)
            if token == '+':
                pos = new_pos
            elif token == '~':
                atom = RuleConstituent(' ', [], POS_TYPE_WORD_FORM, optional=True)
                consequents.append(atom)
                pos = new_pos
            else:
                if pos < len(tokens):
                    atom = RuleConstituent(' ', [], POS_TYPE_WORD_FORM)
                    consequents.append(atom)

        if pos != len(tokens):
            raise Exception("Could not complete parsing the consequents: " + syntax)

        return antecedent, consequents


    def parse_variable(self, tokens: list[str], pos: int):
        token, new_pos = self.parse_token(tokens, pos)
        if token is None:
            return None, 0

        if re.match(self.re_variable, token):
            pos = new_pos
            return token, pos

        return None, 0


    def parse_regexp(self, tokens: list[str], pos: int):
        token, new_pos = self.parse_token(tokens, pos)
        if not token:
            return None, 0

        if token[0] == '/':
            pos = new_pos
            return token[1:-1].replace('\\/', '/'), pos

        return None, 0


    def parse_string(self, tokens: list[str], pos: int):
        token, new_pos = self.parse_token(tokens, pos)
        if not token:
            return None, 0

        if token[0] == "'":
            pos = new_pos
            return token[1:-1].replace("\\'", "'"), pos

        if token[0] == '"':
            pos = new_pos
            return token[1:-1].replace('\\"', '"'), pos

        return None, 0


    def parse_atom(self, tokens: list[str], pos: int):
        predicate, new_pos = self.parse_identifier(tokens, pos)
        if not predicate:
            return None, 0
        pos = new_pos

        open, new_pos = self.parse_token(tokens, pos)
        if open != "(":
            return None, 0
        pos = new_pos

        terms = []
        while True:

            term, new_pos = self.parse_variable(tokens, pos)
            if not term:
                break
            pos = new_pos
            terms.append(term)

            comma, new_pos = self.parse_token(tokens, pos)
            if comma != ",":
                break
            pos = new_pos

        open, new_pos = self.parse_token(tokens, pos)
        if open != ")":
            return None, 0
        pos = new_pos

        return RuleConstituent(predicate, terms, POS_TYPE_RELATION), pos


    def parse_identifier(self, tokens: list[str], pos: int):
        token, new_pos = self.parse_token(tokens, pos)
        if not token:
            return None, 0

        if re.match(self.re_identifier, token):
            pos = new_pos
            return token, pos

        return None, 0


    def parse_token(self, tokens: list[str], pos: int):
        if pos >= len(tokens):
            return None, 0

        return tokens[pos], pos + 1
