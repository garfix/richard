import hashlib
import pickle
from richard.interface.SomeDataSource import SomeDataSource


ID = 'id'
TEXT = 'text'
CONSTANT = 'constant'


class SparqlDataSource(SomeDataSource):

    url: str
    result_cache_path: dict
    headers: list


    def __init__(self, url: str, result_cache_path: bool=None, headers: list={}):
        self.url = url
        self.result_cache_path = result_cache_path
        self.headers = headers


    def select(self, table: str, columns: list[str], values: list) -> list[list]:

        # try to read from results cache
        if self.result_cache_path:
            input_string = table + str(columns) + str(values)
            cache_key = hashlib.sha1(input_string.encode()).hexdigest()
            file_name = self.result_cache_path + "/" + cache_key + ".pickle"
            try:
                with open(file_name, 'rb') as file:
                    result = pickle.load(file)
                    return result
            except OSError as e:
                pass

        # the actual select
        result = self.do_select(table, columns, values)

        # write to the results cache
        if self.result_cache_path:
            try:
                with open(file_name, 'wb') as file:
                    pickle.dump(result, file)
                    return result
            except OSError:
                pass

        return result


    def do_select(self, table: str, columns: list[str], values: list) -> list[list]:

        import requests

        terms = [
            self.prepare_term(values[0], 0, columns),
            self.prepare_term(values[1], 1, columns)
        ]

        variables = self.prepare_variables(values, terms)
        text_variables = self.prepare_text_variables(values, terms, columns)

        # create the sparql query
        query = self.create_query(variables, text_variables, terms, table)

        # Set the parameters for the request
        params = {
            'query': query,
            'format': 'json'  # Get the results in JSON format
        }

        print(query)
        # exit()

        # Send the request to the Wikidata SPARQL endpoint
        # print(self.headers)
        # exit()
        response = requests.get(self.url, params=params, headers=self.headers)

        # print(response)
        # print(response.headers)

        if response.status_code == 403:
            raise Exception("Not allowed: " + str(response.text))
        if response.status_code == 429:
            raise Exception("Too many requests: " + str(response.text))
        if response.status_code == 400:
            raise Exception("Bad request: " + str(response.text))

        # print(response.json())

        # Parse the JSON response
        data = response.json()

        # create results from response data
        results = self.prepare_results(data, values, terms)

        return results


    def create_query(self, variables: list[str], text_variables: list[str], terms: list, table: str):

        locale_filter = ""

        for text_variable in text_variables:
            locale_filter += """
                FILTER(LANG({}) = "en") .
            """.format(text_variable)

        query = """
            SELECT {} WHERE {{
                {} {} {} .
                {}
            }}
        """.format(" ".join(variables), terms[0], table, terms[1], locale_filter)

        return query


    def prepare_term(self, term: any, index: int, columns: list[str]):
        if term == None:
            prepared = "?term" + str(index)
        elif isinstance(term, str):
            if columns[index] == ID:
                prepared = "<{}>".format(term)
            elif columns[index] == CONSTANT:
                prepared = term
            else:
                # todo: locale
                prepared = "'{}'@en".format(term)
        else:
            prepared = str(term)
        return prepared


    def prepare_variables(self, values, terms):
        variables = []
        for i in range(2):
            if values[i] == None:
                variables.append(terms[i])
        if len(variables) == 0:
            variables = ["*"]
        return variables


    def prepare_text_variables(self, values, terms, columns):
        variables = []
        for i in range(2):
            if values[i] == None and columns[i] == TEXT:
                variables.append(terms[i])
        return variables


    def prepare_results(self, data: dict, values: list, terms: list):
        results = []
        for item in data['results']['bindings']:

            result = []
            for i in range(2):
                if values[i] == None:
                    # drop the preceding '?'
                    var = terms[i][1:]
                    value = item[var]['value']
                    result.append(value)
                else:
                    result.append(values[i])

            results.append(result)
        return results
