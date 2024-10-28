from richard.core.constants import IGNORED


class Relation:
    predicate: str
    relation_size: str
    argument_sizes: list[str]
    query_function: callable
    write_function: callable
    attributes: list[str]


    def __init__(self,
        predicate: str,
        attributes: list[str] = None,
        query_function: callable = None,
        write_function: callable = None,
        relation_size: str = IGNORED,
        argument_sizes: list[str] = [],
    ) -> None:
        self.predicate = predicate
        self.query_function = query_function
        self.relation_size = relation_size
        self.argument_sizes = argument_sizes
        self.write_function = write_function
        self.attributes = attributes
