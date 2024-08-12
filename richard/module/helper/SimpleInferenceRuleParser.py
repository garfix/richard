import re

from richard.entity.Variable import Variable
from richard.type.InferenceRule import InferenceRule


class SimpleInferenceRuleParser:

    re_tokens: re.Pattern
    re_identifier: re.Pattern
    re_variable: re.Pattern


    def __init__(self) -> None:
        self.re_tokens = re.compile("(\.|,|:-|\(|\)|'\w+'|[A-Z]\w*|\w+)")
        self.re_identifier = re.compile("^\w+$")
        self.re_variable = re.compile("^[A-Z]\w*$")


    def parse(self, text: str):

        tokens = re.findall(self.re_tokens, text)

        pos = 0
        antecedent, new_pos = self.parse_atom(tokens, pos)
        if not antecedent:
            return None
        pos = new_pos
        
        consequents = []
        implies, new_pos = self.parse_token(tokens, pos)
        if implies == ':-':
            pos = new_pos

            while True:

                consequent, new_pos = self.parse_atom(tokens, pos)
                if not consequent:
                    break
                pos = new_pos
                consequents.append(consequent)
        
                comma, new_pos = self.parse_token(tokens, pos)
                if comma != ",":
                    break
                pos = new_pos

        dot, new_pos = self.parse_token(tokens, pos)
        if dot == ".":            
            pos = new_pos
        
        return InferenceRule(antecedent, consequents)


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
            return None, 0
        pos = new_pos

        return tuple([predicate] + terms), pos
    

    def parse_identifier(self, tokens: list[str], pos: int):
        token, new_pos = self.parse_token(tokens, pos)
        if re.match(self.re_identifier, token):
            pos = new_pos
            return token, pos
        
        return None, 0


    def parse_term(self, tokens: list[str], pos: int):
        token, new_pos = self.parse_token(tokens, pos)
        if token[0] == "'":
            pos = new_pos
            return token[1:-1], pos
        
        if re.match(self.re_variable, token):
            pos = new_pos
            return Variable(token), pos
        
        return None, 0


    def parse_token(self, tokens: list[str], pos: int):
        if pos >= len(tokens):
            return None, 0
                
        return tokens[pos], pos + 1
