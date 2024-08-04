from richard.entity.Instance import Instance
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


    def find_relation_values(self, relation: str, model_values: list, solver: SomeSolver, binding: dict) -> list[list[Simple]]:       

        rows = []
        handled = False
        for module in self.modules:
            relations = module.get_relations()
            if relation in relations:
                info = relations[relation]
                out_values = info.function(relation, model_values, solver, binding)
                rows.extend(out_values)
                handled = True

        if not handled:
            raise Exception("No relation called '" + relation + "' available in the model")
        
        return rows
    

    def get_types(self, model_values: list):
        types = []
        for value in model_values:
            if isinstance(value, Instance):
                types.append(value.entity)
            else:
                types.append(None)
        return types                

