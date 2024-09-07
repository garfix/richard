from richard.data_source.SparqlDataSource import SparqlDataSource


class WikidataDataSource(SparqlDataSource):

    def __init__(self):
        super().__init__("https://query.wikidata.org/sparql")
