from richard.core.constants import INFINITE
from richard.data_source.SparqlDataSource import CONSTANT, ID, TEXT
from richard.entity.Relation import Relation
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext


class WikidataModule(SomeModule):
    """
    This module wraps several Wikidata predicates
    """

    ds: SomeDataSource


    def __init__(self, data_source: SomeDataSource) -> None:

        self.ds = data_source
        self.relations = {
            "wikidata_label": Relation(query_function=self.wikidata_label, relation_size=INFINITE, argument_sizes=[INFINITE, INFINITE]),
            "wikidata_place_of_birth": Relation(query_function=self.wikidata_place_of_birth, relation_size=INFINITE, argument_sizes=[INFINITE, INFINITE]),
            "wikidata_person": Relation(query_function=self.wikidata_person, relation_size=INFINITE, argument_sizes=[INFINITE, INFINITE]),
        }


    def wikidata_person(self, values: list, context: ExecutionContext) -> list[list]:
        person = values[0]

        # person isa human
        out_values = self.ds.select('wdt:P31', [ID, CONSTANT], [person, 'wd:Q5'])
        return out_values


    def wikidata_label(self, values: list, context: ExecutionContext) -> list[list]:
        person = values[0]
        name = values[1]

        # try with given case
        out_values = self.ds.select('rdfs:label', [ID, TEXT], [person, name])
        if len(out_values) == 0 and name != name.title():
            # try with first letters capitalized
            out_values = self.ds.select('rdfs:label', [ID, TEXT], [person, name.title()])

        if len(out_values) > 0:
            return out_values

        raise Exception("Name not found: " + name)


    def wikidata_place_of_birth(self, values: list, context: ExecutionContext) -> list[list]:
        person = values[0]
        place = values[1]

        if person is None:
            raise Exception("Person ID is required: " + str(values))
        if place is not None:
            raise Exception("Place should be None: " + str(values))

        out_values = self.ds.select('wdt:P19', [ID, ID], [person, place])
        return out_values
