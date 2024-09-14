from richard.entity.ProcessingException import ProcessingException
from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext


class TestModule(SomeModule):

    def __init__(self) -> None:

        self.relations = {
            "resolve_name": Relation(query_function=self.resolve_name),
        }


    def resolve_name(self, values: list, context: ExecutionContext) -> list[list]:
        name = values[0].lower()

        raise ProcessingException("Name not found: " + name)
