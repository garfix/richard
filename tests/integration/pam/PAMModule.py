from richard.entity.Relation import Relation
from richard.entity.Variable import Variable
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.entity.ExecutionContext import ExecutionContext


class PAMModule(SomeModule):

    ds: SomeDataSource


    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("go_through_red_light", query_function=self.simple_entity))
        self.add_relation(Relation("pull_over", query_function=self.simple_entity))
        self.add_relation(Relation("summons", query_function=self.simple_entity))
        self.add_relation(Relation("speeding", query_function=self.simple_entity))
        self.add_relation(Relation("for", query_function=self.simple_entity))
        self.add_relation(Relation("cop", query_function=self.simple_entity))
        self.add_relation(Relation("get", query_function=self.simple_entity))
        self.add_relation(Relation("previous_week", query_function=self.simple_entity))
        self.add_relation(Relation("tell", query_function=self.simple_entity))
        self.add_relation(Relation("if", query_function=self.simple_entity))
        self.add_relation(Relation("he", query_function=self.simple_entity))
        self.add_relation(Relation("another", query_function=self.simple_entity))
        self.add_relation(Relation("violation", query_function=self.simple_entity))
        self.add_relation(Relation("license", query_function=self.simple_entity))
        self.add_relation(Relation("his", query_function=self.simple_entity))
        self.add_relation(Relation("take_away", query_function=self.simple_entity))
        self.add_relation(Relation("remember", query_function=self.simple_entity))
        self.add_relation(Relation("game", query_function=self.simple_entity))
        self.add_relation(Relation("poss", query_function=self.simple_entity))
        self.add_relation(Relation("have_on_oneself", query_function=self.simple_entity))
        self.add_relation(Relation("ticket", query_function=self.simple_entity))
        self.add_relation(Relation("number_of", query_function=self.simple_entity))
        self.add_relation(Relation("them", query_function=self.simple_entity))
        self.add_relation(Relation("give", query_function=self.simple_entity))
        self.add_relation(Relation("whole", query_function=self.simple_entity))
        self.add_relation(Relation("incident", query_function=self.simple_entity))
        self.add_relation(Relation("forget", query_function=self.simple_entity))
        self.add_relation(Relation("happen", query_function=self.simple_entity))
        self.add_relation(Relation("terrific", query_function=self.simple_entity))
        self.add_relation(Relation("football_fan", query_function=self.simple_entity))
        self.add_relation(Relation("take", query_function=self.simple_entity))
        self.add_relation(Relation("drive_away", query_function=self.simple_entity))
        self.add_relation(Relation("resolve_name", query_function=self.resolve_name))
        self.add_relation(Relation("lost", query_function=self.simple_entity))
        self.add_relation(Relation("farmer", query_function=self.simple_entity))
        self.add_relation(Relation("stand", query_function=self.simple_entity))
        self.add_relation(Relation("side", query_function=self.simple_entity))
        self.add_relation(Relation("road", query_function=self.simple_entity))
        self.add_relation(Relation("of", query_function=self.simple_entity))
        self.add_relation(Relation("by", query_function=self.simple_entity))
        self.add_relation(Relation("to", query_function=self.simple_entity))
        self.add_relation(Relation("ask", query_function=self.simple_entity))
        self.add_relation(Relation("be", query_function=self.simple_entity))
        self.add_relation(Relation("male", query_function=self.simple_entity))
        self.add_relation(Relation("person", query_function=self.simple_entity))


    def resolve_name(self, values: list, context: ExecutionContext) -> list[list]:
        name = values[0].lower()
        id = values[1]

        out_values = self.ds.select("entity", ["name", "id"], [name, None])

        if len(out_values) > 0:
            return map(lambda row: [None, row[1]], out_values)
        else:
            # if id is given, a new name is linked to that id
            if isinstance(id, Variable):
                # otherwise a new id is created for the name
                id = context.formal_parameters[1].name
            self.ds.insert("entity", ["name", "id", ], [name, id])
            return [
                [None, id]
            ]


    def simple_entity(self, values: list, context: ExecutionContext) -> list[list]:
        return self.ds.select(context.relation.predicate, ["id"], values)
