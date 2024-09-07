from richard.data_source.SparqlDataSource import SparqlDataSource


class WikidataDataSource(SparqlDataSource):

    def __init__(self, result_cache_path: bool=None):
        """
        It's important to add a proper User Agent or you will get many 403 denied responses
        If you intend to use this data source for your own application, change it to something personal

        see also: https://foundation.wikimedia.org/wiki/Policy:User-Agent_policy
        """
        super().__init__("https://query.wikidata.org/sparql",
            result_cache_path=result_cache_path,
            headers={
                "User-Agent": "Richard/1.0 (https://github.com/garfix/richard; patrick.vanbergen@gmail.com) richard/0.2"
            }
        )

