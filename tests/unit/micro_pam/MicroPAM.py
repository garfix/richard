# Comments

# MicroPAM bindings are in the form [ [name, value], [name, value], ...], but we'll just use a dict

# MicroPAM (p187) ------------------------------------------------------

from tests.unit.micro_pam.cd_functions import instantiate
from tests.unit.micro_pam.mcpam_functions import isa, lhs, match_side, rhs


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


    def __init__(self, init_rules: list, sub_for: list, plans_for: list, instance_of: list):
        self.init_rules = init_rules
        self.sub_for = sub_for
        self.plans_for = plans_for
        self.instance_of = instance_of
        self.inference_rules = instance_of + plans_for + sub_for + init_rules
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
        if isa("goal", cd):
            return self.relate(cd, self.known_themes, self.init_rules, log) or self.relate(cd, self.known_plans, self.sub_for, log)
        elif isa("plan", cd):
            return self.relate(cd, self.known_goals, self.plans_for, log)
        # todo fix
        elif cd[0] == 'use-vehicle-plan':
            return self.relate(cd, self.known_goals, self.plans_for, log)
        elif isa("action", cd):
            return self.relate(cd, self.known_plans, self.instance_of, log)
        else:
            return None


    def relate(self, cd: list, item_list: list, rule_list: list, log: list[str]):
        bindings = {}
        exists1 = False
        for item in item_list:

            exists2 = False
            for rule in rule_list:
                bindings = match_side(rhs(rule), cd, {})
                if bindings is not None and match_side(lhs(rule), item, bindings) is not None:
                    log.append("Confirms prediction from")
                    log.append(item)
                    exists2 = True
                    break
            if exists2:
                exists1 = True
                break

        return exists1


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
            bindings = match_side(rhs(rule), cd, {})
            if bindings is not None:
                break

        if bindings:
            chain.append([cd, rules])
            return instantiate(lhs(rule)[0], bindings)

        return None


    def update_db(self, cd: tuple, log: list[str]):
        log.append(cd)
        self.add_cd(cd)

        if isa("is", cd):
            log.append("---theme")
            self.known_themes.append(cd)
        if isa("goal", cd):
            self.known_goals.append(cd)
        if isa("plan", cd):
            self.known_plans.append(cd)


    def add_cd(self, cd):
        self.data_base.append(cd)


    def clear_globals(self):
        self.known_themes = []
        self.known_goals = []
        self.known_plans = []
        self.data_base = []


