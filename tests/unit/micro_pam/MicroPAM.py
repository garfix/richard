# Comments

# MicroPAM bindings are in the form [ [name, value], [name, value], ...], but we'll just use a dict

# MicroPAM (p187) ------------------------------------------------------

from tests.unit.micro_pam.cd_functions import instantiate
from tests.unit.micro_pam.mcpam_functions import isa, lhs, match_side, rhs


class MicroPAM:

    init_rules: list
    sub_for: list
    plans_for: list
    instof: list
    inference_rules: list

    known_themes: list
    known_goals: list
    known_plans: list

    data_base: list
    current_db: None


    def __init__(self, init_rules: list, sub_for: list, plans_for: list, instof: list):
        self.init_rules = init_rules
        self.sub_for = sub_for
        self.plans_for = plans_for
        self.instof = instof
        self.inference_rules = instof + plans_for + sub_for + init_rules
        self.clear_globals()


    def justify(self, input: list[tuple]):

        print("Trying to explain")

        chain = []
        cd = input

        while True:
            if self.predicted(cd):
                break

            print("Does not confirm prediction")
            chain.append([cd, self.inference_rules[:]])

            cd = self.try_inference(chain)
            if not cd:
                break

        if cd:
            print("Adding inference chain to data base")
            for cd_inf in reversed(chain):
                self.update_db(cd_inf[0])
            self.update_db(cd)
        else:
            print("No inference chain found - adding")
            self.update_db(input)


    def predicted(self, cd: list[tuple]):
        if isa("goal", cd):
            return self.relate(cd, self.known_themes, self.init_rules) or self.relate(cd, self.known_plans, self.sub_for)
        elif isa("plan", cd):
            return self.relate(cd, self.known_goals, self.plans_for)
        elif isa("action"):
            return self.relate(cd, self.known_plans, self.instof)
        else:
            return None


    def relate(self, cd: list, item_list: list, rule_list: list):
        bindings = {}
        exists1 = False
        for item in item_list:

            exists2 = False
            for rule in rule_list:
                bindings = match_side(rhs(rule), cd, [])
                if bindings and match_side(lhs(rule), item, bindings):
                    print("Confirms prediction from")
                    print(item)
                    exists2 = True
                    break
            if exists2:
                exists1 = True
                break

        return exists1


    def try_inference(self, chain: list):
        cd_inf = []
        cd = []
        while True:
            if len(chain) == 0:
                break

            cd_inf = chain.pop()
            cd = self.try_rules(cd_inf[0], cd_inf[1][:], chain)
            if cd is None:
                print("No usable inferences from")
                print(cd_inf[0])

            if cd is None:
                break

        if cd:
            print("Possible explanation assuming")
            print(cd)
            return cd

        return None


    def try_rules(self, cd, rules: list, chain: list):
        rule = None
        bindings = {}
        while True:
            if len(rules) == 0:
                break

            rule = rules.pop()

            bindings = match_side(rhs(rule), cd, [])
            if not bindings:
                break

        if bindings:
            chain.append([cd, rules])
            return instantiate(lhs(rule)[0], bindings)

        return None


    def update_db(self, cd: tuple):
        print(cd)
        self.add_cd(cd)

        if isa("is", cd):
            print("theme")
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
        self.current_bd = None


