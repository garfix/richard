from richard.entity.Relation import Relation
from richard.module.BasicOutputBuffer import BasicOutputBuffer


class TestOutputBuffer(BasicOutputBuffer):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("output_predicate", arguments=["predication", "predicate"]))
        self.add_relation(Relation("output_subject", arguments=["predication", "subject"]))
        self.add_relation(Relation("output_object", arguments=["predication", "object"]))
