class PlanAnalyzer:

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


    def __init__(self, init_rules: list, sub_for: list, plans_for: list, instof: list, inference_rules: list):
        self.init_rules = init_rules
        self.sub_for = sub_for
        self.plans_for = plans_for
        self.instof = instof
        self.inference_rules = inference_rules
        self.clear_globals()


    def justify(self, input: list[tuple]):

        print("Trying to explain")

        chain = []
        cd = input

        while True:
            if self.predicted(cd):
                break

            print("Does not confirm prediction")
            chain.append([cd, self.inference_rules])

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
        if self.isa("goal", cd):
            return self.relate(cd, self.known_themes, self.init_rules) or self.relate(cd, self.known_plans, self.sub_for)
        elif self.isa("plan", cd):
            return self.relate(cd, self.known_goals, self.plans_for)
        elif self.isa("action"):
            return self.relate(cd, self.known_plans, self.instof)
        else:
            return None


    def relate(self, cd: list, item_list: list, rule_list: list):
        bd = []
        exists1 = False
        for item in item_list:

            exists2 = False
            for rule in rule_list:
                bd = match_side(rhs(rule), cd, [])
                if bd and match_side(lhs(rule), item, bd):
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
            cd = self.try_rules(cd_inf[0], cd_inf[1], chain)
            if cd is None:
                print("No usable inferences from")
                print(cd_inf[0])

            if not cd:
                break

        if cd:
            print("Possible explanation assuming")
            print(cd)
            return cd

        return None


    def try_rules(self, cd, rules: list, chain: list):
        while True:
            if len(rules) == 0:
                break

            rule = rules.pop()

            bd = match_side(rhs(rule), cd, [])
            if not bd:
                break

        if bd:
            chain.push([cd, rules])
            return instantiate(lhs(rule)[0], bd)

        return None


    def update_db(self, atom: tuple):
        pass


    def isa(self, type: str, cd: list[tuple]):
        pass


    def clear_globals(self):
        self.known_themes = []
        self.known_goals = []
        self.known_plans = []
        self.data_base = []
        self.current_bd = None


def match_side(side, item, bd):
    pass


def lhs(rule):
    return rule[0]


def rhs(rule):
    return rule[1]


def instantiate(self, pattern, binding_list):
    # binds pattern with bindings. if a variable can't be bound, it's set to NIL
    # page 64
    pass
