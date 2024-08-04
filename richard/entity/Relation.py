from dataclasses import dataclass


@dataclass(frozen=True)
class Relation:
    function: callable
    argument_sizes: list[str]
