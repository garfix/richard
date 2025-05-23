from richard.core.Model import Model
from richard.core.Solver import Solver
from richard.core.constants import CATEGORY_FORMAT, CATEGORY_TEXT, CATEGORY_VALUE, POS_TYPE_WORD_FORM
from richard.entity.GrammarRule import GrammarRule
from richard.entity.GrammarRules import GrammarRules
from richard.interface.SomeGenerator import SomeGenerator
from richard.module.BasicOutputBuffer import BasicOutputBuffer


class BasicGenerator(SomeGenerator):

    grammar: GrammarRules
    solver: Solver
    output_buffer: BasicOutputBuffer


    def __init__(self, grammar: GrammarRules, model: Model, output_buffer: BasicOutputBuffer):
        self.grammar = grammar
        self.solver = Solver(model)
        self.output_buffer = output_buffer


    def generate_output(self):
        output = self.generate_node([], "s", [], False)
        self.output_buffer.clear()
        return output


    def generate_node(self, used_rules: list[int], antecedent_cat: str, antecedent_values: list[any], optional: bool) -> list[str]:

        words = []
        rule, binding, found = self.find_rule(used_rules, antecedent_cat, antecedent_values)

        if found:

            hash = rule.hash
            used_rules.append(hash)

            for i, consequent in enumerate(rule.consequents):
                consequent_vals = self.get_consequent_values(rule, i, binding)
                consequent_result = self.generate_single_consequent(rule, used_rules, consequent.predicate, consequent_vals, rule.consequents[i].position_type, consequent.optional)
                words.append(consequent_result)

                # todo?
                # if consequentValue.IsId() && !consequentValue.Equals(antecedentValue) {
                #     generator.state.MarkGenerated(consequentValue)

        else:
            if not optional:
                raise Exception(f"No rule found for {antecedent_cat}: {antecedent_values}")

        # combine the child results
        all_text = list(filter(lambda word: isinstance(word, str), words))
        if len(all_text) == len(words):
              # all strings: concatencate
              result = "".join(words)
        elif len(words) == 1:
            # single value: pick it
            result = words[0]
        else:
            # return a list of values (rare)
            result = words

        # postprocess (strip, capitalize first letter)
        if rule and rule.post:
            return rule.post(result)
        else:
            return result


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


    def find_rule(self, used_rules: list, antecedent_cat: str, antecedent_values: list[any]):

        found = False
        result_rule = None
        binding = {}

        rules = self.grammar.find_rules(antecedent_cat, len(antecedent_values))

        for rule in rules:

            # example rule:
            # syn: s(E1) -> np(E2) vp(E1)
            # if: [('output_type', 'declarative'), ('output_subject', E1, E2)]

            # rule_antecedent_variable = rule.antecedent.arguments[0]
            binding = {}
            for rule_antecedent_variable, antecedent_value in zip(rule.antecedent.arguments, antecedent_values):
                binding[rule_antecedent_variable] = antecedent_value

            # start the binding with the antecedent variable (in the example: E1)
            # if antecedent_values is not None:
            #     binding[rule_antecedent_variable] = antecedent_values

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


    def generate_single_consequent(self, rule: GrammarRule, used_rules: list[str], category: str, values: list[any], position_type: str, optional: bool) -> list[str]:

        if position_type == POS_TYPE_WORD_FORM:
            result = category
        elif category == CATEGORY_VALUE:
            result = values[0]
        elif category == CATEGORY_TEXT:
            result = str(values[0])
        elif category == CATEGORY_FORMAT:
            result = rule.exec(*values)
        else:
            result = self.generate_node(used_rules, category, values, optional)

        return result
