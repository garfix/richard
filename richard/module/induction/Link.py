from richard.entity.InductionRule import InductionRule
from dataclasses import dataclass


@dataclass(frozen=True)
class Link:
    atoms: list[tuple]
    rules: list[InductionRule]
