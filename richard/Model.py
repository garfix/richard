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
        self.modules = modules
        self.modules.append(CoreModule())


    def find_relation_values(self, relation_name: str, model_values: list, solver: SomeSolver, binding: dict) -> list[list[Simple]]:       

        # db_values = self.dehydrate_values(model_values)
        # db_values = model_values
        # in_types = self.get_types(model_values)

        model_results = []
        handled = False
        for module in self.modules:
            if (relation_name in module.get_relations()):
                out_values = module.interpret_relation(relation_name, model_values, solver, binding)
                # model_values = self.hydrate_values(db_values, out_types)
                model_results.extend(out_values)
                handled = True

        if not handled:
            raise Exception('No relation ' + relation_name + " in model")
        
        return model_results
    

    def get_types(self, model_values: list):
        types = []
        for value in model_values:
            if isinstance(value, Instance):
                types.append(value.entity)
            else:
                types.append(None)
        return types                

