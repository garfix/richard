import re

from richard.core.constants import DISJUNCTION
from richard.entity.Variable import Variable
from richard.type.InferenceRule import InferenceRule


class SimpleInferenceRuleParser:

    re_tokens: re.Pattern
    re_identifier: re.Pattern
    re_variable: re.Pattern


    def __init__(self) -> None:
        self.re_tokens = re.compile("(" + "|".join([
            '\.',
            ',',
            ';',
            ':-',
            '\(',
            '\)',
            '\d+\.\d+',
            '\d+',
            "'(?:\\\\'|[^'])+'",
            '"(?:\\\\"|[^"])+"',
            '[A-Z]\w*',
            '\w+',
            '#.*\n',
        ]) + ")")
        self.re_identifier = re.compile("^\w+$")
        self.re_variable = re.compile("^[A-Z]\w*$")
        self.re_float = re.compile("^\d+\.\d+$")
        self.re_int = re.compile("^\d+$")


    def parse(self, text: str):

        rules = []
        tokens = re.findall(self.re_tokens, text)
        pos = 0

        while True:
            rule, new_pos = self.parse_rule(tokens, pos)
            if rule:
                rules.append(rule)
                pos = new_pos
            else:
                break

        pos = self.eat_trailing_comments(tokens, pos)

        if pos != len(tokens):
            return None, new_pos

        return rules, None


    # father(X, Y) :- parent(X, Y), male(X).
    def parse_rule(self, tokens: list[str], pos: int):

        antecedent, new_pos = self.parse_simple_atom(tokens, pos)
        if not antecedent:
            return None, new_pos
        pos = new_pos

        consequents = []
        implies, new_pos = self.parse_token(tokens, pos)
        if implies == ':-':
            pos = new_pos
            consequents, new_pos = self.parse_atoms(tokens, pos)
            if not consequents:
                return None, new_pos
            pos = new_pos

        dot, new_pos = self.parse_token(tokens, pos)

        if not dot == ".":
            return None, new_pos
        pos = new_pos

        return InferenceRule(antecedent, consequents), pos


    # ( parent(X, Y), parent(Y, Z) )
    # parent(X, Y), parent(Y, Z)
    # ( sibling(X, Y) ; ( brother(X, Y) ; sister(X, Y) )
    def parse_atoms(self, tokens: list[str], pos: int):
        atoms, new_pos = self.parse_grouped_atoms(tokens, pos)
        if atoms:
            pos = new_pos
            return atoms, pos

        atoms, new_pos = self.parse_ungrouped_atoms(tokens, pos)
        if atoms:
            pos = new_pos
            return atoms, pos

        return None, pos


    # parent(X, Y), parent(Y, Z)
    def parse_ungrouped_atoms(self, tokens: list[str], pos: int):
        atoms = []

        while True:
            atom, new_pos = self.parse_atom(tokens, pos)
            if not atom:
                return None, new_pos
            pos = new_pos
            atoms.append(atom)

            comma, new_pos = self.parse_token(tokens, pos)

            if comma != ",":
                break
            pos = new_pos

        return atoms, pos


    # ( parent(X, Y), parent(Y, Z) )
    def parse_grouped_atoms(self, tokens: list[str], pos: int):
        open, new_pos = self.parse_token(tokens, pos)
        if open != "(":
            return None, new_pos
        pos = new_pos

        atoms, new_pos = self.parse_atoms(tokens, pos)
        if not atoms:
            return None, new_pos
        pos = new_pos

        open, new_pos = self.parse_token(tokens, pos)
        if open != ")":
            return None, new_pos
        pos = new_pos

        return atoms, pos


    # ( brother(X, Y) ; sister(X, Y)
    def parse_disjuncted_atom(self, tokens: list[str], pos: int):
        open, new_pos = self.parse_token(tokens, pos)
        if open != "(":
            return None, new_pos
        pos = new_pos

        disjuncts = []

        while True:

            atoms, new_pos = self.parse_atoms(tokens, pos)
            if not atoms:
                return None, new_pos
            pos = new_pos
            disjuncts.append(atoms)

            semicolon, new_pos = self.parse_token(tokens, pos)
            if semicolon != ";":
                break
            pos = new_pos

        open, new_pos = self.parse_token(tokens, pos)
        if open != ")":
            return None, new_pos
        pos = new_pos

        disjunction = (DISJUNCTION, disjuncts)

        return disjunction, pos


    # parent(X, Y)
    # ( brother(X, Y) ; sister(X, Y)
    def parse_atom(self, tokens: list[str], pos: int):

        atom, new_pos = self.parse_simple_atom(tokens, pos)
        if atom:
            pos = new_pos
            return atom, pos

        atom, new_pos = self.parse_disjuncted_atom(tokens, pos)
        if atom:
            pos = new_pos
            return atom, pos

        return None, pos


    # parent(X, Y)
    def parse_simple_atom(self, tokens: list[str], pos: int):
        predicate, new_pos = self.parse_identifier(tokens, pos)
        if not predicate:
            return None, new_pos
        pos = new_pos

        open, new_pos = self.parse_token(tokens, pos)
        if open != "(":
            return None, new_pos
        pos = new_pos

        terms = []
        while True:

            term, new_pos = self.parse_term(tokens, pos)
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
            return None, new_pos
        pos = new_pos

        return tuple([predicate] + terms), pos


    # five_horses
    def parse_identifier(self, tokens: list[str], pos: int):
        token, new_pos = self.parse_token(tokens, pos)
        if not token:
            return None, new_pos

        if re.match(self.re_identifier, token):
            pos = new_pos
            return token, pos

        return None, new_pos


    def parse_term(self, tokens: list[str], pos: int):
        token, new_pos = self.parse_token(tokens, pos)
        if token[0] == "'":
            pos = new_pos
            return token[1:-1].replace("\\'", "'"), pos

        if token[0] == '"':
            pos = new_pos
            return token[1:-1].replace('\\"', '"'), pos

        if re.match(self.re_float, token):
            pos = new_pos
            return float(token), pos

        if re.match(self.re_int, token):
            pos = new_pos
            return int(token), pos

        if re.match(self.re_variable, token):
            pos = new_pos
            return Variable(token), pos

        atoms, new_pos = self.parse_atoms(tokens, pos)
        if atoms is not None:
            pos = new_pos
            return atoms, pos

        return None, pos


    def parse_token(self, tokens: list[str], pos: int):
        if pos >= len(tokens):
            return None, pos

        # skip comment
        token = tokens[pos]
        if token[0] == '#':
            return self.parse_token(tokens, pos+1)

        return tokens[pos], pos + 1


    def eat_trailing_comments(self, tokens: list[str], pos: int):
        token, new_pos = self.parse_token(tokens, pos)
        if token == None:
            pos = new_pos

        return pos
