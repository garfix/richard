from richard.core.constants import POS_TYPE_WORD_FORM
from richard.entity.GrammarRule import GrammarRule


class GrammarRules:

    index: dict[str, dict[int, list[GrammarRule]]]


    def __init__(self, grammar_rules: list[GrammarRule]):
        self.index = {}
        for rule in grammar_rules:
            self.add_rule(rule)


    def add_rule(self, rule: GrammarRule):

        antecedent = rule.antecedent.predicate
        argument_count = len(rule.antecedent.arguments)

        if not antecedent in self.index:
            self.index[antecedent] = {}
        if not argument_count in self.index[antecedent]:
            self.index[antecedent][argument_count] = []

        self.index[antecedent][argument_count].append(rule)


    def find_rules(self, antecedent: str, argument_count: int) -> list[GrammarRule]:
        if antecedent in self.index and argument_count in self.index[antecedent]:
            return self.index[antecedent][argument_count]
        else:
            return []

    def find_argument_counts(self, antecedent: str) -> list[GrammarRule]:
        if antecedent in self.index:
            return self.index[antecedent]
        else:
            return []
