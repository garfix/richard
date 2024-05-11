from richard.constants import POS_TYPE_WORD_FORM
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


    def merge(self, otherRules):
        for m in otherRules.index :
            for r in m :
                for rule in r :
                    self.add_rule(rule)


    def find_rules(self, antecedent: str, argument_count: int) -> list[GrammarRule]:
        if antecedent in self.index and argument_count in self.index[antecedent]:
            return self.index[antecedent][argument_count]
        else:
            return []


    def import_from(self, rules):
        for rules_per_category in rules.index :
            for rulesPerCount in rules_per_category :
                for rule in rulesPerCount :
                    self.add_rule(rule)
