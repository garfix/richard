from richard.entity.Relation import Relation
from richard.module.BasicOutputBuffer import BasicOutputBuffer


class TestSentenceContext(BasicOutputBuffer):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("output_predicate", arguments=["predication", "predicate"]))
        self.add_relation(Relation("output_subject", arguments=["predication", "subject"]))
        self.add_relation(Relation("output_object", arguments=["predication", "object"]))


    # def clear(self):
    #     super().clear()

        # cursor = self.data_source.connection.cursor()

        # cursor.execute("CREATE TABLE output_predicate (predication TEXT, predicate TEXT)")
        # cursor.execute("CREATE TABLE output_subject (predication TEXT, subject TEXT)")
        # cursor.execute("CREATE TABLE output_object (predication TEXT, object TEXT)")

