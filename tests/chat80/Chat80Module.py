from richard.constants import IGNORED, E1, LARGE, MEDIUM, SMALL
from richard.entity.Relation import Relation
from richard.interface import SomeSolver
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from .chat80_relations import continental, flows_from_to, south_of
from .chat80_relations import resolve_name

# model

class Chat80Module(SomeModule):

    ds: SomeDataSource
    a: int

    def __init__(self, data_source: SomeDataSource) -> None:

        self.a = 0
        self.ds = data_source
        self.relations = {
            "river": Relation(self.simple_entity, SMALL, [SMALL]),
            "country": Relation(self.simple_entity, MEDIUM, [MEDIUM]),
            "ocean": Relation(self.simple_entity, SMALL, [SMALL]),
            "sea": Relation(self.simple_entity, SMALL, [SMALL]),
            "city": Relation(self.simple_entity, MEDIUM, [MEDIUM]),
            "continent": Relation(self.simple_entity, SMALL, [SMALL]),
            "capital": Relation(self.capital, MEDIUM, [MEDIUM]),
            "borders": Relation(self.borders, LARGE, [MEDIUM, MEDIUM]),
            "resolve_name": Relation(self.resolve_name, LARGE, [LARGE, LARGE]),
            "of": Relation(self.of, LARGE, [MEDIUM, MEDIUM]),
            "size_of": Relation(self.size_of, IGNORED, [MEDIUM, IGNORED]),
            "where": Relation(self.where, IGNORED, [MEDIUM, MEDIUM]),
            "european": Relation(self.some_continent, MEDIUM, [MEDIUM]),
            "asian": Relation(self.some_continent, MEDIUM, [MEDIUM]),
            "african": Relation(self.some_continent, MEDIUM, [MEDIUM]),
            "american": Relation(self.some_continent, MEDIUM, [MEDIUM]),
            "flows_through": Relation(self.flows_through, MEDIUM, [SMALL, MEDIUM]),
            "south_of": Relation(self.south_of, IGNORED, [MEDIUM, MEDIUM]),
            "in": Relation(self.in_function, IGNORED, [MEDIUM, MEDIUM]),
            "flows_from_to": Relation(self.flows_from_to, IGNORED, [MEDIUM, MEDIUM, MEDIUM]),
            "contains": Relation(self.contains, LARGE, [LARGE, LARGE]),
            "has_population": Relation(self.has_population, MEDIUM, [MEDIUM, IGNORED]),
        }
   
    
    def simple_entity(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        db_values = self.dehydrate_values(values)   
        out_types = [relation]
        out_values = self.ds.select(relation, ["id"], db_values)
        return self.hydrate_values(out_values, out_types)


    def capital(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        db_values = self.dehydrate_values(values)   
        out_types = ["city"]
        out_values = self.ds.select("country", ["capital"], db_values)
        return self.hydrate_values(out_values, out_types)


    def borders(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        db_values = self.dehydrate_values(values)   
        # todo may also be ocean
        out_types = ["country", "country"]
        out_values = self.ds.select("borders", ["country_id1", "country_id2"], db_values)
        out_values.extend(self.ds.select("borders", ["country_id2", "country_id1"], db_values))
        return self.hydrate_values(out_values, out_types)


    def resolve_name(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        # self.a += 1
        # print(self.a)
        db_values = self.dehydrate_values(values)   
        out_values, out_types = resolve_name(self.ds, db_values)
        return self.hydrate_values(out_values, out_types)
    

    def of(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        db_values = self.dehydrate_values(values)   
        out_types = ["city", "country"]
        out_values = self.ds.select("country", ["capital", "id"], db_values)
        return self.hydrate_values(out_values, out_types)

    def size_of(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        db_values = self.dehydrate_values(values)   
        out_types = ["country", None]
        out_values = self.ds.select("country", ["id", "area_div_1000"], db_values)
        return self.hydrate_values(out_values, out_types)


    def where(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        db_values = self.dehydrate_values(values)   
        out_types = ["country", "place"]
        out_values = self.ds.select("country", ["id", "region"], db_values)
        return self.hydrate_values(out_values, out_types)


    def some_continent(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        db_values = self.dehydrate_values(values)   
        out_types = ["country"]
        out_values = continental(self.ds, relation, db_values)     
        return self.hydrate_values(out_values, out_types)


    def flows_through(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        db_values = self.dehydrate_values(values)   
        out_types = ["river", "country"]
        out_values = self.ds.select("contains", ["part", "whole"], db_values)
        return self.hydrate_values(out_values, out_types)


    def south_of(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        db_values = self.dehydrate_values(values)   
        out_types = ["country", "place"]
        out_values = south_of(self.ds, db_values)
        return self.hydrate_values(out_values, out_types)


    def in_function(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        db_values = self.dehydrate_values(values)   
        out_types = ["country", "region"]
        out_values = self.ds.select("contains", ["part", "whole"], db_values)

        part = values[0]
        whole = values[1]
        recurse = solver.solve([("contains", whole, E1), ("in", part, E1)], binding)
        out_values.extend(recurse)
        return self.hydrate_values(out_values, out_types)


    def flows_from_to(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        db_values = self.dehydrate_values(values)   
        out_types = ["river", "counry", "sea"]
        out_values = flows_from_to(self.ds, db_values)
        return self.hydrate_values(out_values, out_types)


    def contains(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        db_values = self.dehydrate_values(values)   
        out_types = ["country", "city"]
        out_values = self.ds.select("contains", ["whole", "part"], db_values)
        return self.hydrate_values(out_values, out_types)


    def has_population(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        db_values = self.dehydrate_values(values)   
        out_types = ["country", None]
        if values[0].entity == 'city':
            out_values = self.ds.select("city", ["id", "population"], db_values)
            out_values = [[row[0], row[1] * 1000] for row in out_values]
        else:
            out_values = self.ds.select("country", ["id", "population"], db_values)
            out_values = [[row[0], row[1] * 1000000] for row in out_values]
        return self.hydrate_values(out_values, out_types)
