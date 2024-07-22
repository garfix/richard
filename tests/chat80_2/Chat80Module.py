from richard.interface import SomeSolver
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.type.Simple import Simple
from tests.chat80_2.chat80_relations import continental, flows_from_to, south_of
from tests.chat80_2.chat80_relations import resolve_name

# model

class Chat80Module(SomeModule):

    ds: SomeDataSource

    def __init__(self, data_source: SomeDataSource) -> None:

        self.ds = data_source


    def get_relations(self) -> list[str]:
        return [
            "river", 
            "country", 
            "ocean",
            "sea",
            "capital", 
            "borders",
            "resolve_name",
            "of",
            "size-of",
            "where",
            "european", "asian", "african", "american",
            "flows-through",
        ]


    def interpret_relation(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        db_values = self.dehydrate_values(values)
    
        if relation == "river":
            out_types = ["river"]
            out_values = self.ds.select("river", ["id"], db_values)
        elif relation == "country":
            out_types = ["country"]
            out_values = self.ds.select("country", ["id"], db_values)
        elif relation == "ocean":
            out_types = ["ocean"]
            out_values = self.ds.select("ocean", ["id"], db_values)
        elif relation == "sea":
            out_types = ["sea"]
            out_values = self.ds.select("sea", ["id"], db_values)
        elif relation == "capital":
            out_types = ["city"]
            out_values = self.ds.select("country", ["capital"], db_values)
        elif relation == "borders":
            # todo may also be ocean
            out_types = ["country", "country"]
            out_values = self.ds.select("borders", ["country_id1", "country_id2"], db_values)
            out_values.extend(self.ds.select("borders", ["country_id2", "country_id1"], db_values))
        elif relation == "of":
            out_types = ["city", "country"]
            out_values = self.ds.select("country", ["capital", "id"], db_values)
        elif relation == "size-of":
            out_types = ["country", None]
            out_values = self.ds.select("country", ["id", "area"], db_values)
        elif relation == "where":
            out_types = ["country", "place"]
            out_values = self.ds.select("country", ["id", "region"], db_values)
        elif relation == "resolve_name":
            out_values, out_types = resolve_name(self.ds, db_values)
        elif relation in ["european", "asian", "african", "american"]:
            out_types = ["country"]
            out_values = continental(self.ds, relation, db_values)     
        elif relation == "flows-through":
            out_types = ["river", "country"]
            out_values = self.ds.select("contains", ["part", "whole"], db_values)
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
            out_values = []

        # print(relation, db_values, out_values)

        return self.hydrate_values(out_values, out_types)
    