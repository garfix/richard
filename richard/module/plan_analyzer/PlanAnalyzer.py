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

    def relate(self):
        pass



    def isa(self, type: str, cd: list[tuple]):
        pass


    def try_inference(self, chain: list):
        pass


    def update_db(self, atom: tuple):
        pass


    def clear_globals(self):
        self.known_themes = []
        self.known_goals = []
        self.known_plans = []
        self.data_base = []
        self.current_bd = None
