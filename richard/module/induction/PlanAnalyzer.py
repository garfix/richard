from richard.core.functions.helper import hash_it
from richard.core.functions.terms import bind_variables
from richard.entity.InferenceRule import InferenceRule
from richard.entity.InductionRule import InductionRule
from richard.entity.ExecutionContext import ExecutionContext
from richard.module.induction.Link import Link
from richard.module.induction.functions import match


# Based on MicroPAM (see https://github.com/garfix/micropam)
class PlanAnalyzer:

    known_themes: list[tuple]
    known_goals: list[tuple]
    known_plans: list[tuple]

    try_check: dict

    def __init__(self):
        self.known_themes = []
        self.known_goals = []
        self.known_plans = []
        self.try_check = {}


    def justify(self, sentence: list[tuple], induction_rules: list[InductionRule], deduction_rules: list[InferenceRule], context: ExecutionContext):

        print('---')

        log = []

        log.append("Trying to explain")
        log.append(sentence)

        chain: list[Link] = []

        current_subject = sentence

        while True:
            if self.predicted(current_subject, induction_rules, deduction_rules, context, log, sentence):
                break

            log.append("Does not confirm prediction")
            chain.append(Link(current_subject, induction_rules[:]))

            current_subject = self.try_inference(chain, deduction_rules, context, log, sentence)
            if not current_subject:
                break

        if current_subject:
            log.append("Adding inference chain to data base")
            for link in reversed(chain):
                self.update_db(link.atoms, context, log)
            self.update_db(current_subject, context, log)
        else:
            log.append("No inference chain found - adding")
            self.update_db(sentence, context, log)

        for line in log:
            print(line)

        print('---')


    def predicted(self, current_subject: list, induction_rules: list[InductionRule], deduction_rules: list[InferenceRule], context: ExecutionContext, log: list[str], sentence):
        # is cd part of the known plans, goals or themes?
        if self.isa("goal", current_subject):
            # return self.relate(sentence, self.known_themes, self.init_rules, deduction_rules, context, log) \
            #     or self.relate(sentence, self.known_plans, self.sub_for, deduction_rules, context, log)
            return self.relate(current_subject, self.known_themes, induction_rules, deduction_rules, context, log, sentence) \
                or self.relate(current_subject, self.known_plans, induction_rules, deduction_rules, context, log, sentence)
        elif self.isa("plan", current_subject):
            # return self.relate(sentence, self.known_goals, self.plans_for, deduction_rules, context, log)
            return self.relate(current_subject, self.known_goals, induction_rules, deduction_rules, context, log, sentence)
        elif self.isa("action", current_subject):
            # return self.relate(sentence, self.known_plans, self.instance_of, deduction_rules, context, log)
            return self.relate(current_subject, self.known_plans, induction_rules, deduction_rules, context, log, sentence)
        else:
            return None


    def relate(self, current_subject: list, item_list: list, induction_rules: list[InductionRule], deduction_rules: list[InferenceRule], context: ExecutionContext, log: list[str], sentence):
        # item_list contains known themes, goals, or plans
        # rule_list contains all rules that belong to the themes, goals or plans
        # each rule has an antecedent (rhs) and a consequent (lhs)
        # the function tries the match the cd (via the antecedent) with the known theme, goal, or plan (via the consequent)
        binding = {}
        for item in item_list:
            for rule in induction_rules:
                binding = match(rule.antecedent, current_subject, {}, deduction_rules, context, sentence)
                # print(' XX antecedent', rule.antecedent)
                # print(' XX binding', binding)
                # if binding is not None:
                    # print()
                    # print(' XX antecedent', rule.antecedent)
                    # print(' XX consequent', rule.consequent)
                    # print(' XX item', item)
                    # print(' XX binding', binding)
                    # a = match(rule.consequent, item, binding, deduction_rules, context, current_subject)
                    # print(' XX result', a)

                if binding is not None:
                    if match(rule.consequent, item, binding, deduction_rules, context, current_subject) is not None:
                        log.append("Confirms prediction from")
                        log.append(item)
                        return True

        return False


    def try_inference(self, chain: list[Link], deduction_rules: list[InferenceRule], context: ExecutionContext, log: list, sentence):
        # chain is a list of [cd, all_inference_rules]
        # return the lhs of the first match, and extend the chain
        current_subject = None
        while len(chain) > 0:
            last_link = chain.pop()
            # try all inference rules in the cd
            # if the cd matches a rule, add it to the chain
            # and return the bound lhs of the rule
            current_subject = self.try_rules(last_link.atoms, last_link.rules[:], chain, deduction_rules, context, sentence)
            if current_subject is None:
                log.append("No usable inferences from")
                log.append(last_link.atoms)
            else:
                break

        if current_subject:
            log.append("Possible explanation assuming")
            log.append(current_subject)
            return current_subject

        return None


    def try_rules(self, current_subject, rules: list[InductionRule], chain: list[Link], deduction_rules: list[InferenceRule], context: ExecutionContext, sentence):
        # match cd with the rhs of each of the rules
        # if a match occurs, return a binding with the lhs of the rule
        last_rule = None
        binding = None
        while len(rules) > 0:
            last_rule = rules.pop()
            binding = match(last_rule.antecedent, current_subject, {}, deduction_rules, context, sentence)

            # if the combination of antecedent and binding has happened before, skip it
            hash = hash_it([last_rule.antecedent, binding])
            # print(hash, last_rule.antecedent, sentence, binding)
            if hash in self.try_check:
                continue
            else:
                self.try_check[hash] = True

            if binding is not None:
                break

        if binding:
            # append the fact to the chain
            chain.append(Link(current_subject, rules))
            return bind_variables(last_rule.consequent, binding)

        return None


    def update_db(self, sentence: list[tuple], context: ExecutionContext, log: list):
        log.append(sentence)

        # add cd as a fact to the `database`
        context.solver.write_atoms(sentence)

        # add cd to the known themes, goals or plans
        # if self.isa("is", sentence):
        #     log.append("---theme")
        #     self.known_themes.append(sentence)
        if self.isa("goal", sentence):
            self.known_goals.append(sentence)
        elif self.isa("plan", sentence):
            self.known_plans.append(sentence)
        else:
            log.append("---theme")
            # note: in MicroPAM only sentences with "is" are stored as themes (i.e. only the first sentence)
            self.known_themes.append(sentence)


    def isa(self, type: str, current_subject: any):
        predicate = current_subject[0][0]
        return predicate == type
