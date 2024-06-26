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

        db_values = self.dehydrate_values(model_values)
        in_types = self.get_types(model_values)

        model_results = []
        handled = False
        for module in self.modules:
            if (relation_name in module.get_relations()):
                db_values, out_types = module.interpret_relation(relation_name, db_values, in_types, solver, binding)
                model_values = self.hydrate_values(db_values, out_types)
                model_results.extend(model_values)
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

        
    def dehydrate_values(self, values: list[Simple]) -> list[Simple]:
        dehydrated = []
        for value in values:
            if isinstance(value, Instance):
                dehydrated.append(value.id)
            else:
                dehydrated.append(value)
        return dehydrated


    def hydrate_values(self, rows: list[list], types: list[str]) -> list:
        hydrated = []
        for values in rows:
            new_row = []
            for value, type in zip(values, types):
                if type is not None:
                    new_row.append(Instance(type, value))
                else:
                    new_row.append(value)
            hydrated.append(new_row)
        return hydrated
