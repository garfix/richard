from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.module.CoreModule import CoreModule
from richard.interface.SomeSolver import SomeSolver
from richard.type.Simple import Simple


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


    def find_relation_values(self, predicate: str, model_values: list, solver: SomeSolver, binding: dict) -> list[list[Simple]]:       

        relations = self.find_relations(predicate)
        if len(relations) == 0:
            raise Exception("No relation called '" + predicate + "' available in the model")

        rows = []
        for relation in relations:
            out_values = relation.function(predicate, model_values, solver, binding)
            rows.extend(out_values)
        
        return rows
    