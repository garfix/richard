# Comments

# MicroPAM bindings are in the form [ [name, value], [name, value], ...], but we'll just use a dict

# MicroPAM (p187) ------------------------------------------------------

from tests.unit.micro_pam.cd_functions import filler_role, header_cd, instantiate, match
from tests.unit.micro_pam.extra_functions import is_predication
from tests.unit.micro_pam.lisp_functions import atom, numberp
from tests.unit.micro_pam.mcpam_functions import constraint_side, lhs, pattern_side, rhs


class MicroPAM:

    init_rules: list
    sub_for: list
    plans_for: list
    instance_of: list
    inference_rules: list

    known_themes: list
    known_goals: list
    known_plans: list

    data_base: list

    isa_props: dict


    def __init__(self, init_rules: list, sub_for: list, plans_for: list, instance_of: list, isa_props: dict):
        self.init_rules = init_rules
        self.sub_for = sub_for
        self.plans_for = plans_for
        self.instance_of = instance_of
        self.inference_rules = instance_of + plans_for + sub_for + init_rules
        self.isa_props = isa_props
        self.clear_globals()


    def justify(self, input: list[tuple], log: list[str]):
        """
        Tries to find an explanation for `input` (a CD predication)
        """

        log.append("Trying to explain")
        log.append(input)

        chain = []
        cd = input

        while True:
            if self.predicted(cd, log):
                break

            log.append("Does not confirm prediction")
            chain.append([cd, self.inference_rules[:]])

            cd = self.try_inference(chain, log)
            if not cd:
                break

        if cd:
            log.append("Adding inference chain to data base")
            for cd_inf in reversed(chain):
                self.update_db(cd_inf[0], log)
            self.update_db(cd, log)
        else:
            log.append("No inference chain found - adding")
            self.update_db(input, log)


    def predicted(self, cd: list[tuple], log: list[str]):
        if self.isa("goal", cd):
            return self.relate(cd, self.known_themes, self.init_rules, log) or self.relate(cd, self.known_plans, self.sub_for, log)
        elif self.isa("plan", cd):
            return self.relate(cd, self.known_goals, self.plans_for, log)
        elif self.isa("action", cd):
            return self.relate(cd, self.known_plans, self.instance_of, log)
        else:
            return None


    def relate(self, cd: list, item_list: list, rule_list: list, log: list[str]):
        bindings = {}
        for item in item_list:
            for rule in rule_list:
                bindings = self.match_side(rhs(rule), cd, {})
                if bindings is not None and self.match_side(lhs(rule), item, bindings) is not None:
                    log.append("Confirms prediction from")
                    log.append(item)
                    return True

        return False


    def try_inference(self, chain: list, log: list[str]):
        cd_inf = []
        cd = None
        while True:
            if len(chain) == 0:
                break

            cd_inf = chain.pop()
            cd = self.try_rules(cd_inf[0], cd_inf[1][:], chain)
            if cd is None:
                log.append("No usable inferences from")
                log.append(cd_inf[0])

            if cd:
                break

        if cd:
            log.append("Possible explanation assuming")
            log.append(cd)
            return cd

        return None


    def try_rules(self, cd, rules: list, chain: list):
        rule = None
        bindings = {}
        while True:
            if len(rules) == 0:
                break

            rule = rules.pop()
            bindings = self.match_side(rhs(rule), cd, {})
            if bindings is not None:
                break

        if bindings:
            chain.append([cd, rules])
            return instantiate(lhs(rule)[0], bindings)

        return None


    def update_db(self, cd: tuple, log: list[str]):
        log.append(cd)
        self.add_cd(cd)

        if self.isa("is", cd):
            log.append("---theme")
            self.known_themes.append(cd)
        if self.isa("goal", cd):
            self.known_goals.append(cd)
        if self.isa("plan", cd):
            self.known_plans.append(cd)


    def add_cd(self, cd):
        self.data_base.append(cd)


    def match_side(self, side, item, bindings: dict) -> dict:

        current_bindings = match(pattern_side(side), item, bindings)

        if current_bindings:
            if constraint_side(side):
                if not self.evaluate(constraint_side(side), current_bindings):
                    return None

        return current_bindings


    def evaluate(self, cd, bindings: dict):
        if is_predication(cd):
            predicate = cd[0]
            if predicate == "pos-val":
                value = instantiate(cd[1], bindings)
                return value[0] > 0
            elif predicate == "isa":
                an_instance = instantiate(cd[1], bindings)
                a_class = instantiate(cd[2], bindings)
                return self.isa(an_instance, a_class)
            else:
                raise Exception(f"Unknown predicate for 'evaluate': {predicate}")

        return False


    def isa(self, type: str, cd: any):
        if numberp(cd):
            return False
        elif atom(cd):
            return self.isa_check(type, cd)
        else:
            if self.isa_check(type, header_cd(cd)):
                return True
            x = filler_role("type", cd)
            if x:
                return self.isa_check(type, header_cd(x))

        return False


    def isa_check(self, type, cd):
        if type == cd:
            return True
        if cd in self.isa_props and self.isa_props[cd] == type:
            return True
        return False


    def clear_globals(self):
        self.known_themes = []
        self.known_goals = []
        self.known_plans = []
        self.data_base = []


