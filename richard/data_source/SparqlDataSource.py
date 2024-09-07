from richard.interface.SomeDataSource import SomeDataSource

ID = 'id'
TEXT = 'text'

class SparqlDataSource(SomeDataSource):

    url: str

    def __init__(self, url: str):
        self.url = url


    def select(self, table: str, columns: list[str], values: list) -> list[list]:

        import requests

        terms = [
            self.prepare_term(values[0], 0, columns),
            self.prepare_term(values[1], 1, columns)
        ]

        variables = self.prepare_variables(values, terms)

        # create the sparql query
        query = self.create_query(variables, terms, table)

        # Set the parameters for the request
        params = {
            'query': query,
            'format': 'json'  # Get the results in JSON format
        }

        print(query)
        # exit()

        # Send the request to the Wikidata SPARQL endpoint
        response = requests.get(self.url, params=params)

        # print(response)
        # print(response.headers)

        if response.status_code == 403:
            raise Exception("Not allowed: " + str(response.text))
        if response.status_code == 429:
            raise Exception("Too many requests: " + str(response.text))

        # print(response.json())

        # Parse the JSON response
        data = response.json()

        # create results from response data
        results = self.prepare_results(data, values, terms)

        return results


    def create_query(self, variables: list[str], terms: list, table: str):
        query = """
            SELECT {} WHERE {{
                {} {} {}
            }}
        """.format(" ".join(variables), terms[0], table, terms[1])

        return query


    def prepare_term(self, term: any, index: int, columns: list[str]):
        if term == None:
            prepared = "?term" + str(index)
        elif isinstance(term, str):
            if columns[index] == ID:
                prepared = "<{}>".format(term)
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
            variables = ["1"]
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
