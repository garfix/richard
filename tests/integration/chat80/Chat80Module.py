from richard.core.constants import IGNORED, E1, LARGE, MEDIUM, SMALL
from richard.entity.Relation import Relation
from richard.entity.Variable import Variable
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.entity.ExecutionContext import ExecutionContext


class Chat80Module(SomeModule):

    ds: SomeDataSource


    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("river", query_function=self.simple_entity, relation_size=SMALL, argument_sizes=[SMALL]))
        self.add_relation(Relation("country", query_function=self.simple_entity, relation_size=MEDIUM, argument_sizes=[MEDIUM]))
        self.add_relation(Relation("ocean", query_function=self.simple_entity, relation_size=SMALL, argument_sizes=[SMALL]))
        self.add_relation(Relation("sea", query_function=self.simple_entity, relation_size=SMALL, argument_sizes=[SMALL]))
        self.add_relation(Relation("city", query_function=self.simple_entity, relation_size=MEDIUM, argument_sizes=[MEDIUM]))
        self.add_relation(Relation("continent", query_function=self.simple_entity, relation_size=SMALL, argument_sizes=[SMALL]))
        self.add_relation(Relation("capital", query_function=self.capital, relation_size=MEDIUM, argument_sizes=[MEDIUM]))
        self.add_relation(Relation("borders", query_function=self.borders, relation_size=LARGE, argument_sizes=[MEDIUM, MEDIUM]))
        self.add_relation(Relation("resolve_name", query_function=self.resolve_name, relation_size=LARGE, argument_sizes=[LARGE, LARGE]))
        self.add_relation(Relation("of", query_function=self.of, relation_size=LARGE, argument_sizes=[MEDIUM, MEDIUM]))
        self.add_relation(Relation("size_of", query_function=self.size_of, relation_size=IGNORED, argument_sizes=[MEDIUM, IGNORED]))
        self.add_relation(Relation("where", query_function=self.where, relation_size=IGNORED, argument_sizes=[MEDIUM, MEDIUM]))
        self.add_relation(Relation("european", query_function=self.some_continent, relation_size=MEDIUM, argument_sizes=[MEDIUM]))
        self.add_relation(Relation("asian", query_function=self.some_continent, relation_size=MEDIUM, argument_sizes=[MEDIUM]))
        self.add_relation(Relation("african", query_function=self.some_continent, relation_size=MEDIUM, argument_sizes=[MEDIUM]))
        self.add_relation(Relation("american", query_function=self.some_continent, relation_size=MEDIUM, argument_sizes=[MEDIUM]))
        self.add_relation(Relation("flows_through", query_function=self.flows_through, relation_size=MEDIUM, argument_sizes=[SMALL, MEDIUM]))
        self.add_relation(Relation("south_of", query_function=self.south_of, relation_size=IGNORED, argument_sizes=[MEDIUM, MEDIUM]))
        self.add_relation(Relation("flows_from_to", query_function=self.flows_from_to, relation_size=MEDIUM, argument_sizes=[MEDIUM, MEDIUM, MEDIUM]))
        self.add_relation(Relation("contains", query_function=self.contains, relation_size=MEDIUM, argument_sizes=[MEDIUM, MEDIUM]))
        self.add_relation(Relation("has_population", query_function=self.has_population, relation_size=MEDIUM, argument_sizes=[MEDIUM, IGNORED]))


    def simple_entity(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.ds.select(context.relation.predicate, ["id"], arguments)


    def capital(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.ds.select("country", ["capital"], arguments)


    def borders(self, arguments: list, context: ExecutionContext) -> list[list]:
        out_values = self.ds.select("borders", ["country_id1", "country_id2"], arguments)
        out_values.extend(self.ds.select("borders", ["country_id2", "country_id1"], arguments))
        return out_values


    def of(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.ds.select("country", ["capital", "id"], arguments)


    def size_of(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.ds.select("country", ["id", "area_div_1000"], arguments)


    def where(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.ds.select("country", ["id", "region"], arguments)


    def some_continent(self, arguments: list, context: ExecutionContext) -> list[list]:
        country_id = arguments[0]
        table = "country"
        columns = ["id", "region"]
        regions = {
            "european": ['southern_europe', 'western_europe', 'eastern_europe', 'scandinavia'],
            "asian": ['middle_east', 'indian_subcontinent', 'southeast_east', 'far_east', 'northern_asia'],
            "american": ['north_america', 'central_america', 'caribbean', 'south_america'],
            "african": ['north_africa', 'west_africa', 'central_africa', 'east_africa', 'southern_africa']
        }

        out_values = []
        for region in regions[context.relation.predicate]:
            ids = self.ds.select_column(table, columns, [country_id, region])
            for id in ids:
                out_values.append([id])

        return out_values


    def flows_through(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.ds.select("contains", ["part", "whole"], arguments)


    def south_of(self, arguments: list, context: ExecutionContext) -> list[list]:
        # this implementation could be done in SQL like "SELECT id FROM country WHERE lat < (SELECT lat FROM country WHERE id = %s)"
        id1 = arguments[0]
        id2 = arguments[1]
        lat1 = None
        lat2 = None
        latitudes = self.ds.select('country', ['id', 'lat'], [Variable("E1"), Variable("E2")])
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


    def in_function(self, arguments: list, context: ExecutionContext) -> list[list]:
        out_values = self.ds.select("contains", ["part", "whole"], arguments)

        part = arguments[0]
        whole = arguments[1]
        recurse = context.solver.solve([("contains", whole, E1), ("in", part, E1)])
        out_values.extend(recurse)
        return out_values


    def flows_from_to(self, arguments: list, context: ExecutionContext) -> list[list]:
        query_river = arguments[0]
        query_from = arguments[1]
        query_to = arguments[2]
        flows = self.ds.select('river', ['id', 'flows_through'], [Variable("E1"), Variable("E2")])
        out_values = []
        for id, flows_through in flows:
            flows_through_elements = flows_through.split("|")
            db_to = flows_through_elements[0]
            db_from = flows_through_elements[1:2]
            if isinstance(query_river, Variable) or id == query_river:
                if isinstance(query_to, Variable) or query_to == db_to:
                    if isinstance(query_from, Variable) or query_from in db_from:
                        for f in db_from:
                            out_values.append([id, f, db_to])

        return out_values


    def contains(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.ds.select("contains", ["whole", "part"], arguments)


    def has_population(self, arguments: list, context: ExecutionContext) -> list[list]:

        out_values = self.ds.select("city", ["id", "population"], arguments)
        pops1 = [[row[0], row[1] * 1000] for row in out_values]

        out_values = self.ds.select("country", ["id", "population"], arguments)
        pops2 = [[row[0], row[1] * 1000000] for row in out_values]

        return pops1 + pops2


    def resolve_name(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[0].lower()

        for type in ["country", "city", "sea", "river", "ocean", "continent"]:
            out_values = self.ds.select(type, ["id", "id"], [name, Variable("E1")])
            if len(out_values) > 0:
                return [[None, value[1]] for value in out_values]

        if name == 'equator':
            return [[None, 'equator']]


        context.solver.solve([('store', [('output_type', 'name_not_found'), ('output_name_not_found', name)])])
        return []
