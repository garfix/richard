from richard.data_source.SimpleDataSource import SimpleDataSource
from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class BasicOutputBuffer(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()

        self.add_relation(Relation("output_type", arguments=["type"]))
        self.add_relation(Relation("output_value", arguments=["value"]))
        self.add_relation(Relation("output_value_with_unit", arguments=["value", "unit"]))
        self.add_relation(Relation("output_table", arguments=["results", "units"]))
        self.add_relation(Relation("output_list", arguments=["elements"]))
        self.add_relation(Relation("output_name_not_found", arguments=["name"]))
        self.add_relation(Relation("output_unknown_word", arguments=["word"]))


    def clear(self):
        self.data_source = SimpleDataSource()
