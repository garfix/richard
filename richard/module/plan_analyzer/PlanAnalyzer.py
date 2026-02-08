from richard.core.atoms import reify_variables, unification
from richard.entity.Variable import Variable
from richard.entity.ExecutionContext import ExecutionContext


# Based on MicroPAM (see https://github.com/garfix/micropam)
class PlanAnalyzer:

    known_themes: list[tuple]
    known_goals: list[tuple]
    known_plans: list[tuple]


    def __init__(self):
        self.known_themes = []
        self.known_goals = []
        self.known_plans = []


    def justify(self, sentence: list[tuple], context: ExecutionContext):

        current_sentence = sentence

        while True:
            if self.predicted(current_sentence):
                break

            current_sentence = self.try_inference()
            if not current_sentence:
                break

        if current_sentence:
            pass
        else:
            self.update_db(sentence, context)


    def predicted(self, sentence: list[tuple]):
        return False


    def try_inference(self):
        return False


    def update_db(self, sentence: list[tuple], context: ExecutionContext):
        reified = reify_variables(sentence)

        print(reified)

        if unification(sentence, [('goal', Variable('E1'))]):
            self.known_goals.append(reified)
        else:
            self.known_themes.append(reified)

