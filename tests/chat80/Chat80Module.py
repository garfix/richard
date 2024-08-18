from richard.constants import IGNORED, E1, LARGE, MEDIUM, SMALL
from richard.entity.Relation import Relation
from richard.entity.Variable import Variable
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext


class Chat80Module(SomeModule):

    ds: SomeDataSource


    def __init__(self, data_source: SomeDataSource) -> None:

        self.ds = data_source
        self.relations = {
            "river": Relation(query_function=self.simple_entity, relation_size=SMALL, argument_sizes=[SMALL]),
            "country": Relation(query_function=self.simple_entity, relation_size=MEDIUM, argument_sizes=[MEDIUM]),
            "ocean": Relation(query_function=self.simple_entity, relation_size=SMALL, argument_sizes=[SMALL]),
            "sea": Relation(query_function=self.simple_entity, relation_size=SMALL, argument_sizes=[SMALL]),
            "city": Relation(query_function=self.simple_entity, relation_size=MEDIUM, argument_sizes=[MEDIUM]),
            "continent": Relation(query_function=self.simple_entity, relation_size=SMALL, argument_sizes=[SMALL]),
            "capital": Relation(query_function=self.capital, relation_size=MEDIUM, argument_sizes=[MEDIUM]),
            "borders": Relation(query_function=self.borders, relation_size=LARGE, argument_sizes=[MEDIUM, MEDIUM]),
            "resolve_name": Relation(query_function=self.resolve_name, relation_size=LARGE, argument_sizes=[LARGE, LARGE]),
            "of": Relation(query_function=self.of, relation_size=LARGE, argument_sizes=[MEDIUM, MEDIUM]),
            "size_of": Relation(query_function=self.size_of, relation_size=IGNORED, argument_sizes=[MEDIUM, IGNORED]),
            "where": Relation(query_function=self.where, relation_size=IGNORED, argument_sizes=[MEDIUM, MEDIUM]),
            "european": Relation(query_function=self.some_continent, relation_size=MEDIUM, argument_sizes=[MEDIUM]),
            "asian": Relation(query_function=self.some_continent, relation_size=MEDIUM, argument_sizes=[MEDIUM]),
            "african": Relation(query_function=self.some_continent, relation_size=MEDIUM, argument_sizes=[MEDIUM]),
            "american": Relation(query_function=self.some_continent, relation_size=MEDIUM, argument_sizes=[MEDIUM]),
            "flows_through": Relation(query_function=self.flows_through, relation_size=MEDIUM, argument_sizes=[SMALL, MEDIUM]),
            "south_of": Relation(query_function=self.south_of, relation_size=IGNORED, argument_sizes=[MEDIUM, MEDIUM]),
            "flows_from_to": Relation(query_function=self.flows_from_to, relation_size=IGNORED, argument_sizes=[MEDIUM, MEDIUM, MEDIUM]),
            "contains": Relation(query_function=self.contains, relation_size=LARGE, argument_sizes=[LARGE, LARGE]),
            "has_population": Relation(query_function=self.has_population, relation_size=MEDIUM, argument_sizes=[MEDIUM, IGNORED]),
        }


    def simple_entity(self, values: list, context: ExecutionContext) -> list[list]:
        return self.ds.select(context.predicate, ["id"], values)


    def capital(self, values: list, context: ExecutionContext) -> list[list]:
        return self.ds.select("country", ["capital"], values)


    def borders(self, values: list, context: ExecutionContext) -> list[list]:
        out_values = self.ds.select("borders", ["country_id1", "country_id2"], values)
        out_values.extend(self.ds.select("borders", ["country_id2", "country_id1"], values))
        return out_values


    def of(self, values: list, context: ExecutionContext) -> list[list]:
        return self.ds.select("country", ["capital", "id"], values)


    def size_of(self, values: list, context: ExecutionContext) -> list[list]:
        return self.ds.select("country", ["id", "area_div_1000"], values)


    def where(self, values: list, context: ExecutionContext) -> list[list]:
        return self.ds.select("country", ["id", "region"], values)


    def some_continent(self, values: list, context: ExecutionContext) -> list[list]:
        country_id = values[0]
        table = "country"
        columns = ["id", "region"]
        regions = {
            "european": ['southern_europe', 'western_europe', 'eastern_europe', 'scandinavia'],
            "asian": ['middle_east', 'indian_subcontinent', 'southeast_east', 'far_east', 'northern_asia'],
            "american": ['north_america', 'central_america', 'caribbean', 'south_america'],
            "african": ['north_africa', 'west_africa', 'central_africa', 'east_africa', 'southern_africa']
        }

        out_values = []
        for region in regions[context.predicate]:
            ids = self.ds.select_column(table, columns, [country_id, region])
            for id in ids:
                out_values.append([id])

        return out_values


    def flows_through(self, values: list, context: ExecutionContext) -> list[list]:
        return self.ds.select("contains", ["part", "whole"], values)


    def south_of(self, values: list, context: ExecutionContext) -> list[list]:
        # this implementation could be done in SQL like "SELECT id FROM country WHERE lat < (SELECT lat FROM country WHERE id = %s)"
        id1 = values[0]
        id2 = values[1]
        lat1 = None
        lat2 = None
        latitudes = self.ds.select('country', ['id', 'lat'], [None, None])
        latitudes.append(['equator', 0])
        for id, lat in latitudes:
            if id == id1:
                lat1 = lat
            if id == id2:
                lat2 = lat
        if id1 and id2:
            if lat1 < lat2:
                out_values = [[id1, id2]]
            else:
                out_values = []
        elif id2 and not id1:
            out_values = [[id, id2] for id, lat in latitudes if lat < lat2]
        else:
            raise Exception("Unhandled case")

        return out_values


    def in_function(self, values: list, context: ExecutionContext) -> list[list]:
        out_values = self.ds.select("contains", ["part", "whole"], values)

        part = values[0]
        whole = values[1]
        recurse = context.solver.solve([("contains", whole, E1), ("in", part, E1)], context.binding)
        out_values.extend(recurse)
        return out_values


    def flows_from_to(self, values: list, context: ExecutionContext) -> list[list]:
        query_river = values[0]
        query_from = values[1]
        query_to = values[2]
        flows = self.ds.select('river', ['id', 'flows_through'], [None, None])
        out_values = []
        for id, flows_through in flows:
            db_to = flows_through[0]
            db_from = flows_through[1:2]
            if not id or id == query_river:
                if not query_to or query_to == db_to:
                    if not query_from or query_from in db_from:
                        for f in db_from:
                            out_values.append([id, f, db_to])

        return out_values


    def contains(self, values: list, context: ExecutionContext) -> list[list]:
        return self.ds.select("contains", ["whole", "part"], values)


    def has_population(self, values: list, context: ExecutionContext) -> list[list]:
        term = context.arguments[0]
        type = ""
        if isinstance(term, Variable):
            isas = context.solver.solve([('isa', term.name, Variable('Type'))])
            if len(isas) > 0:
                type = isas[0]["Type"]

        if type == 'city':
            out_values = self.ds.select("city", ["id", "population"], values)
            out_values = [[row[0], row[1] * 1000] for row in out_values]
        else:
            out_values = self.ds.select("country", ["id", "population"], values)
            out_values = [[row[0], row[1] * 1000000] for row in out_values]
        return out_values


    def resolve_name(self, values: list, context: ExecutionContext) -> list[list]:
        name = values[0].lower()

        for type in ["country", "city", "sea", "river", "ocean", "continent"]:
            out_values = self.ds.select(type, ["id", "id"], [name, None])
            if len(out_values) > 0:
                context.solver.write_atom(('isa', context.arguments[1].name, type))
                return out_values

        if name == 'equator':
            return [['equator', 'equator']]


        raise Exception("Name not found: " + name)
