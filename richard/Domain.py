from dataclasses import dataclass

from richard.interface.SomeDb import SomeDb


@dataclass(frozen=True)
class Domain:
    """
    This class represents the state of the world, and is the source of truth for the pipeline
    """
    
    dbs: list[SomeDb]
