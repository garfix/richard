# Based on MicroPAM (see https://github.com/garfix/micropam)
from richard.core.atoms import reify_variables
from richard.entity.ExecutionContext import ExecutionContext


class PlanAnalyzer:

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
        for atom in sentence:
            reified = reify_variables(atom)
            print(reified)
            context.solver.write_atom(reified)


