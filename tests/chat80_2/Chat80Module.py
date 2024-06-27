from richard.interface import SomeSolver
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.type.Simple import Simple
from tests.chat80.chat80_relations import continental, flows_from_to, south_of

# model

class Chat80Module(SomeModule):

    ds: SomeDataSource

    def __init__(self, data_source: SomeDataSource) -> None:

        self.ds = data_source


    def get_relations(self) -> list[str]:
        return [
            "river", 
            "borders",
        ]


    def interpret_relation(self, relation_name: str, db_values: list, in_types: list[str], solver: SomeSolver, binding: dict) -> list[list]:
    
        if relation_name == "river":
            out_types = ["river"]
            db_values = self.ds.select("river", ["id"], db_values)
        elif relation_name == "borders":
            out_types = ["country", "country"]
            db_values = self.ds.select("borders", ["country_id1", "country_id2"], db_values)
        # elif relation == "flows-through":
        #     return self.ds.select("contains", ["part", "whole"], values)
        # elif relation == "contains":
        #     if model_values[1].entity == "city":
        #         return self.ds.select("city", ["country", "id"], values)
        #     else:
        #         return self.ds.select("contains", ["part", "whole"], values)
        # elif relation == "in":
        #     return self.ds.select("contains", ["part", "whole"], values)
        # elif relation == "south-of":
        #     return south_of(self.ds, values)
        # elif relation == "flows-from-to":
        #     return flows_from_to(self.ds, values)
        # else:
        #     raise Exception("No table found for " + relation)
        else:
            out_types = []
            db_values = []
      
        return db_values, out_types
    

