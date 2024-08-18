from richard.constants import IGNORED


class Relation:

    query_function: callable
    relation_size: str
    argument_sizes: list[str]
    write_function: callable
    attributes: list[str]


    def __init__(self,
        attributes: list[str] = None,
        query_function: callable = None,
        write_function: callable = None,
        relation_size: str = IGNORED,
        argument_sizes: list[str] = [],
    ) -> None:
        self.query_function = query_function
        self.relation_size = relation_size
        self.argument_sizes = argument_sizes
        self.write_function = write_function
        self.attributes = attributes
