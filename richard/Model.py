from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.module.CoreModule import CoreModule


class Model:
    """
    This class represents the generic part of the model.
    """

    modules: list[SomeModule]


    def __init__(
            self, 
            modules: list[SomeModule]
    ) -> None:
        self.modules = [CoreModule()]
        self.modules.extend(modules)


    def find_relations(self, relation: str) -> list[Relation]:
        result = []
        for module in self.modules:
            relations = module.get_relations()
            if relation in relations:
                result.append(relations[relation])
        return result
