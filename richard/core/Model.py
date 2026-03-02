from richard.entity.Relation import Relation
from richard.interface.SomeModel import SomeModel
from richard.interface.SomeModule import SomeModule
from richard.module.CoreModule import CoreModule


class Model(SomeModel):
    """
    This class represents the generic part of the model.
    """

    modules: list[SomeModule]


    def __init__(
            self,
            modules: list[SomeModule]
    ) -> None:
        self.modules = [
            CoreModule(),
        ]
        self.modules.extend(modules)


    def find_relations(self, predicate: str) -> list[Relation]:
        result = []
        for module in self.modules:
            relation = module.get_relation(predicate)
            if relation:
                result.append(relation)
        return result


