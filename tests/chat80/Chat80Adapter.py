from richard.ModelAdapter import ModelAdapter
from richard.entity.Modifier import Modifier
from richard.entity.Attribute import Attribute
from richard.entity.Entity import Entity
from richard.entity.Relation import Relation
from richard.interface.SomeDataSource import SomeDataSource
from richard.type.Simple import Simple
from tests.chat80.chat80_relations import continental, south_of

# model

class Chat80Adapter(ModelAdapter):

    ds: SomeDataSource

    def __init__(self, data_source: SomeDataSource) -> None:

        self.ds = data_source

        super().__init__(
            modifiers=[
                Modifier("european"),
                Modifier("asian"),
                Modifier("american"),
                Modifier("african"),
            ],
            # todo(?): include attributes with entities, because their argument types may be different
            # todo: multiple attributes with the same name but different argument types
            attributes=[
                Attribute("size-of", [None, "country"]),
                Attribute("capital-of", ["city", "country"]),
                Attribute("location-of", ["place", "country"])
            ],
            entities=[
                Entity("place", [], []),
                Entity("river", [], []),
                Entity("country", ["size-of", "capital-of", "location-of"], ["european", "asian", "american", "african"]),
                Entity("city", ["size-of"], []),
                Entity("ocean", [], []),
                Entity("sea", [], []),
                Entity("circle_of_latitude", [], []),
                Entity("region", [], []),
                Entity("continent", [], []),
            ], 
            relations=[
                Relation("borders", ['country', 'country']),
                Relation("flows-through", ['river', 'country']),
                Relation("south-of", ['place', 'place']),
                Relation("in", ['place', 'place']),
            ], 
        )


    def interpret_relation(self, relation: str, values: list[Simple]) -> list[list[Simple]]:
        if relation == "borders":
            return self.ds.select("borders", ["country_id1", "country_id2"], values)
        elif relation == "flows-through":
            return self.ds.select("contains", ["part", "whole"], values)
        elif relation == "in":
            return self.ds.select("contains", ["part", "whole"], values)
        elif relation == "south-of":
            return south_of(self.ds, values)
        else:
            raise Exception("No table found for " + relation)
    

    def interpret_entity(self, entity: str) -> list[Simple]:
        return self.ds.select_column(entity, ['id'], [None])
    

    def interpret_attribute(self, entity: str, attribute: str, values: list[Simple]) -> list[Simple]:
        if attribute == "capital-of":
            return self.ds.select("country", ["capital", "id"], values)
        elif attribute == "size-of":
            return self.ds.select("country", ["area", "id"], values)
        elif attribute == "location-of":
            return self.ds.select("country", ["region", "id"], values)
        else:
            raise Exception("No table found for " + entity)
    

    def interpret_modifier(self, entity: str, modifier: str, value: Simple) -> list[Simple]:
        if entity == "country":
            if modifier in ["european", "asian", "african", "american"] :
                return continental(self.ds, modifier, value)     
        else:
            raise Exception("No table found for " + entity + ":" + modifier)

