from richard.constants import IGNORED


class Relation:

    function: callable
    relation_size: str
    argument_sizes: list[str]
    

    def __init__(self, function: callable, relation_size: str = IGNORED, argument_sizes: list[str] = []) -> None:
        self.function = function
        self.relation_size = relation_size
        self.argument_sizes = argument_sizes
