from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class BasicSentenceContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        # self.add_relation(Relation("format", arguments=["type"]))
        # self.add_relation(Relation("format_list", arguments=["variable"]))
        # self.add_relation(Relation("format_table", arguments=["variable", "unit"]))
        # self.add_relation(Relation("format_number", arguments=["variable", "unit"]))
        # self.add_relation(Relation("format_canned", arguments=["response"]))
        # self.add_relation(Relation("format_no", arguments=["response"]))
        # self.add_relation(Relation("format_yes", arguments=["response"]))
        # self.add_relation(Relation("format_switch", arguments=["variable", "default_template"]))
        # self.add_relation(Relation("format_switch_value", arguments=["value", "template"]))

        self.add_relation(Relation("output_type", arguments=["type"]))


    def clear(self):
        super().clear()

        cursor = self.data_source.connection.cursor()

        # cursor.execute("CREATE TABLE format (type TEXT)")
        # cursor.execute("CREATE TABLE format_list (variable TEXT)")
        # cursor.execute("CREATE TABLE format_table (variable TEXT, unit TEXT)")
        # cursor.execute("CREATE TABLE format_number (variable TEXT, unit TEXT)")
        # cursor.execute("CREATE TABLE format_canned (response TEXT)")
        # cursor.execute("CREATE TABLE format_no (response TEXT)")
        # cursor.execute("CREATE TABLE format_yes (response TEXT)")
        # cursor.execute("CREATE TABLE format_switch (variable TEXT, default_template TEXT)")
        # cursor.execute("CREATE TABLE format_switch_value (value TEXT, template TEXT)")

        cursor.execute("CREATE TABLE output_type (type TEXT)")