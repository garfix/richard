from richard.constants import BLOCKED, E1
from richard.entity.Relation import Relation
from richard.interface import SomeSolver
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.type.Simple import Simple
from .chat80_relations import continental, flows_from_to, south_of
from .chat80_relations import resolve_name

# model

class Chat80Module(SomeModule):

    ds: SomeDataSource

    def __init__(self, data_source: SomeDataSource) -> None:

        self.ds = data_source
        self.relations = {
            "river": Relation(self.simple_entity, [BLOCKED, BLOCKED, BLOCKED]),
            "country": Relation(self.simple_entity, [BLOCKED, BLOCKED, BLOCKED]),
            "ocean": Relation(self.simple_entity, [BLOCKED, BLOCKED, BLOCKED]),
            "sea": Relation(self.simple_entity, [BLOCKED, BLOCKED, BLOCKED]),
            "city": Relation(self.simple_entity, [BLOCKED, BLOCKED, BLOCKED]),
            "continent": Relation(self.simple_entity, [BLOCKED, BLOCKED, BLOCKED]),
            "capital": Relation(self.capital, [BLOCKED, BLOCKED, BLOCKED]),
            "borders": Relation(self.borders, [BLOCKED, BLOCKED, BLOCKED]),
            "resolve_name": Relation(self.resolve_name, [BLOCKED, BLOCKED, BLOCKED]),
            "of": Relation(self.of, [BLOCKED, BLOCKED, BLOCKED]),
            "size-of": Relation(self.size_of, [BLOCKED, BLOCKED, BLOCKED]),
            "where": Relation(self.where, [BLOCKED, BLOCKED, BLOCKED]),
            "european": Relation(self.some_continent, [BLOCKED, BLOCKED, BLOCKED]),
            "asian": Relation(self.some_continent, [BLOCKED, BLOCKED, BLOCKED]),
            "african": Relation(self.some_continent, [BLOCKED, BLOCKED, BLOCKED]),
            "american": Relation(self.some_continent, [BLOCKED, BLOCKED, BLOCKED]),
            "flows-through": Relation(self.flows_through, [BLOCKED, BLOCKED, BLOCKED]),
            "south-of": Relation(self.south_of, [BLOCKED, BLOCKED, BLOCKED]),
            "in": Relation(self.in_function, [BLOCKED, BLOCKED, BLOCKED]),
            "flows-from-to": Relation(self.flows_from_to, [BLOCKED, BLOCKED, BLOCKED]),
            "contains": Relation(self.contains, [BLOCKED, BLOCKED, BLOCKED]),
            "has-population": Relation(self.has_population, [BLOCKED, BLOCKED, BLOCKED]),
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
