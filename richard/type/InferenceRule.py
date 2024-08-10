from dataclasses import dataclass

from richard.entity.RuleConstituent import RuleConstituent


@dataclass(frozen=True)
class InferenceRule:
    head: tuple
    body: list[tuple]
    

    def __str__(self) -> str:
        if len(self.body) == 0:
            return str(self.head) + "."
        else:
            return str(self.head) + " :- " + ", ".join([(str(atom)) for atom in self.body]) + "."
    