import re
from richard.core.constants import IGNORED


class Relation:
    predicate: str
    relation_size: str
    argument_sizes: list[str]
    query_function: callable
    write_function: callable
    arguments: list[str]


    def __init__(self,
        predicate: str,
        arguments: list[str] = None,
        query_function: callable = None,
        write_function: callable = None,
        relation_size: str = IGNORED,
        argument_sizes: list[str] = [],
    ) -> None:
        if not re.fullmatch('[\w_]+', predicate):
            raise Exception('Predicate is not a word: ' + predicate)

        self.predicate = predicate
        self.query_function = query_function
        self.relation_size = relation_size
        self.argument_sizes = argument_sizes
        self.write_function = write_function
        self.arguments = arguments
