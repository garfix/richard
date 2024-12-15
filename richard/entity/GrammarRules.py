import copy
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

        # create a variant of the rule for all permutations of optional constituents
        for variant in self.create_rule_variants(rule):
            self.index[antecedent][argument_count].append(variant)


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


    def create_rule_variants(self, rule: GrammarRule) -> list[GrammarRule]:
        consequent_variants = self.create_rule_variants_rest(rule, 0, [[]])

        variants = []
        for consequent_variant in consequent_variants:
            new_rule = copy.copy(rule)
            new_rule.consequents = consequent_variant
            variants.append(new_rule)

        return variants


    def create_rule_variants_rest(self, rule: GrammarRule, index: 0, variants: list[list]) -> list[GrammarRule]:
        if index == len(rule.consequents):
            return variants

        consequent = rule.consequents[index]

        new_variants = [v + [consequent] for v in variants]

        if consequent.optional:
            new_variants.extend(variants)

        return self.create_rule_variants_rest(rule, index+1, new_variants)
