import hashlib
import pickle
from richard.data_source.SparqlDataSource import SparqlDataSource


class WikidataDataSource(SparqlDataSource):

    result_cache_path: dict

    def __init__(self, result_cache_path: bool=None):
        super().__init__("https://query.wikidata.org/sparql")
        self.result_cache_path = result_cache_path


    def select(self, table: str, columns: list[str], values: list) -> list[list]:

        if self.result_cache_path:
            input_string = table + str(columns) + str(values)
            cache_key = hashlib.sha1(input_string.encode()).hexdigest()
            file_name = self.result_cache_path + "/" + cache_key + ".pickle"
            try:
                print(file_name)
                with open(file_name, 'rb') as file:
                    result = pickle.load(file)
                    return result
            except OSError as e:
                print(str(e))
                pass

        result = super().select(table, columns, values)

        if self.result_cache_path:
            try:
                with open(file_name, 'wb') as file:
                    pickle.dump(result, file)
                    return result
            except OSError:
                pass

        return result
