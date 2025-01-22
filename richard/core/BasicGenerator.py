from richard.core.Model import Model
from richard.core.Solver import Solver
from richard.core.constants import CATEGORY_FORMAT, CATEGORY_TEXT, CATEGORY_VALUE, POS_TYPE_WORD_FORM
from richard.entity.GrammarRule import GrammarRule
from richard.entity.GrammarRules import GrammarRules
from richard.interface.SomeGenerator import SomeGenerator


class BasicGenerator(SomeGenerator):

    grammar: GrammarRules
    solver: Solver


    def __init__(self, grammar: GrammarRules, model: Model):
        self.grammar = grammar
        self.solver = Solver(model)


    def generate_output(self):
        words = self.generate_node([], "s", None)
        all_text = list(filter(lambda word: isinstance(word, str), words))
        if len(words) == 1:
            return words[0]
        elif len(all_text) == len(words):
              return "".join(words)
        else:
            return words


    def generate_node(self, used_rules: list[int], antecedent_cat: str, antecedent_val: any) -> list[str]:

        words = []
        rule, binding, ok = self.find_rule(used_rules, antecedent_cat, antecedent_val)

        if ok:

            hash = rule.hash
            used_rules.append(hash)

            for i, consequent in enumerate(rule.consequents):
                consequent_vals = self.get_consequent_values(rule, i, binding)
                consequent = self.generate_single_consequent(rule, used_rules, consequent.predicate, consequent_vals, rule.consequents[i].position_type)
                words.extend(consequent)

                # todo?
                # if consequentValue.IsId() && !consequentValue.Equals(antecedentValue) {
                #     generator.state.MarkGenerated(consequentValue)


        return words


    def get_consequent_values(self, rule: GrammarRule, i: int, binding: dict) -> any:
        consequent_values = []

        consequent = rule.consequents[i]
        for a in range(len(consequent.arguments)):
            if consequent.position_type == POS_TYPE_WORD_FORM:
                consequent_value = ""
            else:
                consequent_variable = consequent.arguments[a]
                if consequent_variable in binding:
                    consequent_value = binding[consequent_variable]
                else:
                    consequent_value = ""

            consequent_values.append(consequent_value)

        return consequent_values


    def find_rule(self, used_rules: list, antecedent_cat: str, antecedent_val: any):

        found = False
        result_rule = None
        binding = {}

        rules = self.grammar.find_rules(antecedent_cat, 1)

        for rule in rules:

            # example rule:
            # syn: s(E1) -> np(E2) vp(E1)
            # if: [('output_type', 'declarative'), ('output_subject', E1, E2)]

            rule_antecedent_variable = rule.antecedent.arguments[0]
            binding = {}

            # start the binding with the antecedent variable (in the example: E1)
            if antecedent_val is not None:
                binding[rule_antecedent_variable] = antecedent_val

            if not rule.sem:
                # no condition
                result_rule = rule
                found = True

            else:

                # match the condition
                # will bind the E2 in the example ([('output_type', 'declarative'), ('output_subject', E1, E2)])
                match_bindings = self.solver.solve(rule.sem, binding)

                if len(match_bindings) > 0:
                    binding = match_bindings[0]
                    result_rule = rule
                    found = True


            if found:
                # make sure the same rule is not executed again and again
                if rule.hash not in used_rules:
                    break

        return result_rule, binding, found


    def generate_single_consequent(self, rule: GrammarRule, used_rules: list[str], category: str, values: list[any], position_type: str) -> list[str]:

        words = []

        if position_type == POS_TYPE_WORD_FORM:
            words.append(category)
        elif category == CATEGORY_VALUE:
            words.append(values[0])
        elif category == CATEGORY_TEXT:
            words.append(str(values[0]))
        elif category == CATEGORY_FORMAT:
            result = rule.exec(*values)
            words.append(result)
        else:
            words = self.generate_node(used_rules, category, values[0])

        return words
