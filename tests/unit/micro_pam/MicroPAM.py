# Comments

# MicroPAM bindings are in the form [ [name, value], [name, value], ...], but we'll just use a dict

# MicroPAM (p187) ------------------------------------------------------

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


# -- McPAM helper functions (p189) ------------------------------------------------------

def match_side(side, item, bindings: dict) -> dict:
    current_bindings = match(pattern_side(side), item, bindings)
    # todo: strange: latest current_bd
    return current_bindings and evaluate(constraint_side(side)) and current_bindings


def isa(type: str, cd: any):
    if numberp(cd):
        return False
    elif atom(cd):
        return isa_check(type, cd)
    else:
        if isa_check(type, header_cd(cd)):
            return True
        x = filler_role("type", cd)
        if isa_check(type, header_cd, x):
            return True

    return False


def isa_check(type, x):
    return type == x or type == get(x, "isa")


def pos_val(cd):
    if consp(cd):
        cd = cd[0]
        if numberp(cd):
            return not minusp(cd) and cd != 0


def lhs(rule):
    return rule[0]


def rhs(rule):
    return rule[1]


def pattern_side(side):
    return side[0]


def constraint_side(side):
    if side[1]:
        return side[1][0]
    return None


# -- CD functions (p63) --------------------------------------------------------

def filler_role(role, cd):
    # looks for the pair (role filler) in the cd, and returns the filler
    # like this (?)
    for item in cd:
        if isinstance(item, list) and len(item) > 0 and item[0] == role:
            return item[1]

    return None


def header_cd(cd):
    # returns the main predicate of a cd form
    # (?)
    return cd[0]


def instantiate(self, pattern, bindings: dict):
    # binds pattern with bindings. if a variable can't be bound, it's set to NIL
    # page 64
    pass


def match(pattern, cd, bindings: dict):
    # if pattern matches cd, then the binding list is returned, with any new bindings added
    new_bindings = bindings.copy()
    if is_predication_list(pattern) and is_predication_list(cd):
        # each predication in pattern should match at least one in cd
        for p in pattern:
            found = False
            for c in cd:
                b = match(p, c, bindings)
                if b is not None:
                    found = True
                    new_bindings = merge_bindings(bindings, b)
                    break
            if not found:
                new_bindings = None
    elif is_predication(pattern) and is_predication(cd):
        if len(pattern) != len(cd):
            new_bindings = None
        for p, c in zip(pattern, cd):
            b = match(p, c, bindings)
            if b is not None:
                new_bindings = merge_bindings(bindings, b)
            else:
                new_bindings = None
                break
    elif is_variable(pattern):
        variable = pattern[1:]
        new_bindings = merge_bindings(bindings, {variable: cd})
    else:
        if pattern != cd:
            new_bindings = None

    print(pattern, cd, bindings, new_bindings)

    return new_bindings


def merge_bindings(bindings1: dict, bindings2: dict) -> dict:
    if bindings1 is None:
        return None

    new_bindings = bindings1.copy()
    for key, value in bindings2.items():
        if key in bindings1 and bindings1[key] != bindings2[key]:
            return None
        new_bindings[key] = value

    return new_bindings


# -- Lisp functions (p54) ------------------------------------------------------

def atom(cd):
    return isinstance(cd, str) or isinstance(cd, int) or isinstance(cd, float)


def consp(cd):
    return None if atom(cd) else cd


def evaluate(cd):
    if isinstance(cd, list):
        # example; may not be needed
        if cd[0] == "plus":
            return cd[1] + cd[2]

    return None


def get(object, property):
    # depends on the structure of an object (?)
    return object[property]


def minusp(cd):
    return cd < 0


def numberp(cd):
    return isinstance(cd, int) or isinstance(cd, float)


# -- additional helper functions for the Python port ---------------------------

# ['person', ['name', 'John']]
def is_predication(cd):
    return isinstance(cd, list) and len(cd) > 1 and isinstance(cd[0], str)


# "?x"
def is_variable(cd):
    return isinstance(cd, str) and len(cd) > 0 and cd[0] == '?'


# [ ["name", "John"], ["profession", "barber"] ]
def is_predication_list(cd):
    return isinstance(cd, list) and len(cd) > 0 and is_predication(cd[0])
