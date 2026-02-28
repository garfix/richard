from richard.entity.InductionRule import InductionRule
from richard.entity.ExecutionContext import ExecutionContext
from richard.module.induction.Link import Link
from richard.module.induction.functions import instantiate, match


# Based on MicroPAM (see https://github.com/garfix/micropam)
class PlanAnalyzer:

    known_themes: list[tuple]
    known_goals: list[tuple]
    known_plans: list[tuple]


    def __init__(self):
        self.known_themes = []
        self.known_goals = []
        self.known_plans = []


    def justify(self, sentence: list[tuple], induction_rules: list[InductionRule], context: ExecutionContext):

        current_sentence = sentence

        chain: list[Link] = []
        log = []

        while True:
            if self.predicted(current_sentence, log):
                break

            chain.append(Link(current_sentence, induction_rules[:]))

            current_sentence = self.try_inference(chain, log)
            if not current_sentence:
                break

        if current_sentence:
            pass
        else:
            self.update_db(sentence, context, log)


    def predicted(self, sentence: list, log: list[str]):
        # is cd part of the known plans, goals or themes?
        if self.isa("goal", sentence):
            return self.relate(sentence, self.known_themes, self.init_rules, log) or self.relate(sentence, self.known_plans, self.sub_for, log)
        elif self.isa("plan", sentence):
            return self.relate(sentence, self.known_goals, self.plans_for, log)
        elif self.isa("action", sentence):
            return self.relate(sentence, self.known_plans, self.instance_of, log)
        else:
            return None


    def relate(self, sentence: list, item_list: list, rule_list: list[InductionRule], log: list[str]):
        # item_list contains known themes, goals, or plans
        # rule_list contains all rules that belong to the themes, goals or plans
        # each rule has an antecedent (rhs) and a consequent (lhs)
        # the function tries the match the cd (via the antecedent) with the known theme, goal, or plan (via the consequent)
        bindings = {}
        for item in item_list:
            for rule in rule_list:
                bindings = match(rule.antecedent, sentence, {})
                if bindings is not None and match(rule.consequent, item, bindings) is not None:
                    log.append("Confirms prediction from")
                    log.append(item)
                    return True

        return False


    def try_inference(self, chain: list[Link], log: list):
        # chain is a list of [cd, all_inference_rules]
        # return the lhs of the first match, and extend the chain
        sentence = None
        while len(chain) > 0:
            last_link = chain.pop()
            # try all inference rules in the cd
            # if the cd matches a rule, add it to the chain
            # and return the bound lhs of the rule
            sentence = self.try_rules(last_link.atoms, last_link.rules[:], chain)
            if sentence is None:
                log.append("No usable inferences from")
                log.append(last_link.atoms)
            else:
                break

        if sentence:
            log.append("Possible explanation assuming")
            log.append(sentence)
            return sentence

        return None


    def try_rules(self, sentence, rules: list[InductionRule], chain: list[Link]):
        # match cd with the rhs of each of the rules
        # if a match occurs, return a binding with the lhs of the rule
        last_rule = None
        bindings = None
        while len(rules) > 0:
            last_rule = rules.pop()
            bindings = match(last_rule.antecedent, sentence, {})
            if bindings is not None:
                break

        if bindings:
            # append the fact to the chain
            chain.append([sentence, rules])
            return instantiate(last_rule.consequent, bindings)

        return None


    def update_db(self, sentence: list[tuple], context: ExecutionContext, log: list):
        log.append(sentence)

        # add cd as a fact to the `database`
        context.solver.write_atoms(sentence)

        # add cd to the known themes, goals or plans
        if self.isa("is", sentence):
            log.append("---theme")
            self.known_themes.append(sentence)
        if self.isa("goal", sentence):
            self.known_goals.append(sentence)
        if self.isa("plan", sentence):
            self.known_plans.append(sentence)


    def isa(self, type: str, cd: any):
        raise Exception("todo")
