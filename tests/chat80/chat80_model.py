from richard.ModelAdapter import ModelAdapter
from richard.Model import Model
from richard.entity.Modifier import Modifier
from richard.entity.Attribute import Attribute
from richard.entity.Entity import Entity
from richard.entity.Relation import Relation
from richard.type.Simple import Simple
from .chat80_db import ds

# model

class Chat80Adapter(ModelAdapter):
    def __init__(self) -> None:
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
                Entity("region", [], [])
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
            table = "borders"
            columns = ["country_id1", "country_id2"]
        elif relation == "flows-through":
            table = "contains"
            columns = ["part", "whole"]
        elif relation == "in":
            table = "contains"
            columns = ["part", "whole"]
        elif relation == "south-of":
            return self.south_of(values)
        else:
            raise Exception("No table found for " + relation)
        
        return ds.select(table, columns, values)
    

    def interpret_entity(self, entity: str) -> list[Simple]:
        return ds.select_column(entity, ['id'], [None])
    

    def interpret_attribute(self, entity: str, attribute: str, values: list[Simple]) -> list[Simple]:
        table = None
        if attribute == "capital-of":
            table = "country"
            columns = ["capital", "id"]
        if attribute == "size-of":
            table = "country"
            columns = ["area", "id"]
        if attribute == "location-of":
            table = "country"
            columns = ["region", "id"]

        if not table:
            raise Exception("No table found for " + attribute)

        return ds.select(table, columns, values)
    

    def interpret_modifier(self, entity: str, modifier: str, value: Simple) -> list[Simple]:
        table = None
        if entity == "country":
            if modifier in ["european", "asian", "african", "american"] :
                table = "country"
                columns = ["id", "region"]
                regions = {
                    "european": ['southern_europe', 'western_europe', 'eastern_europe', 'scandinavia'],
                    "asian": ['middle_east', 'indian_subcontinent', 'southeast_east', 'far_east', 'northern_asia'],
                    "american": ['north_america', 'central_america', 'caribbean', 'south_america'],
                    "african": ['north_africa', 'west_africa', 'central_africa', 'east_africa', 'southern_africa']
                }

                ids = []
                for region in regions[modifier]:
                    ids += ds.select_column(table, columns, [value, region])
                return ids
            
        if not table:
            raise Exception("No table found for " + entity + ":" + modifier)

        return ds.select_column(table, columns, [value])
    

    def south_of(self, values: list[Simple]):
        # this implementation could be done in SQL like "SELECT id FROM country WHERE lat < (SELECT lat FROM country WHERE id = %s)"
        id1 = values[0]
        id2 = values[1]
        lat1 = None
        lat2 = None
        latitudes = ds.select('country', ['id', 'lat'], [None, None])
        latitudes.append(['equator', 0])
        for id, lat in latitudes:
            if id == id1:
                lat1 = lat
            if id == id2:
                lat2 = lat
        if id1 and id2:
            if lat1 < lat2:
                return [[id1, id2]]
            else:
                return []
        if id2 and not id1:
            return [[id, id2] for id, lat in latitudes if lat < lat2]
        raise Exception("Unhandled case")
                

model = Model(Chat80Adapter())
