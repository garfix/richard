import csv
from richard.interface.SomeDataSource import SomeDataSource


class CsvImporter:
    def import_table_from_file(self, table_name: str, file_path: str, data_source: SomeDataSource):
        with open(file_path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            line = 0
            headers = []
            for row in reader:
                if len(row) == 0:
                    continue
                line += 1
                if line == 1:
                    headers = row
                    # print(headers)
                else:
                    values = []
                    for header, element in zip(headers, row):
                        # # a | implements an array of values
                        # if "|" in element:
                        #     element = element.split("|")
                        # # integer
                        # elif element.lstrip("-+").isdigit():
                        #     element = int(element)
                        values.append(element)

                    # print(values)
                    data_source.insert(table_name, headers, values)
