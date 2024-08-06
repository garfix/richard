from dataclasses import dataclass


@dataclass(frozen=True)
class Relation:
    function: callable
    relation_size: str
    argument_sizes: list[str]
