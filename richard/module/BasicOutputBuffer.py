from richard.data_source.SimpleDataSource import SimpleDataSource
from richard.entity.Relation import Relation
from richard.module.SqliteMemoryModule import SqliteMemoryModule


class BasicOutputBuffer(SqliteMemoryModule):

    def __init__(self) -> None:
        super().__init__()

        self.add_relation(Relation("output_type", formal_parameters=["type"]))
        self.add_relation(Relation("output_value", formal_parameters=["value"]))
        self.add_relation(Relation("output_value_with_unit", formal_parameters=["value", "unit"]))
        self.add_relation(Relation("output_table", formal_parameters=["results", "units"]))
        self.add_relation(Relation("output_list", formal_parameters=["elements"]))
        self.add_relation(Relation("output_name_not_found", formal_parameters=["name"]))
        self.add_relation(Relation("output_unknown_word", formal_parameters=["word"]))


    def clear(self):
        self.data_source = SimpleDataSource()
