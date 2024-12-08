from dataclasses import dataclass

from richard.entity.RuleConstituent import RuleConstituent
from richard.entity.Variable import Variable


@dataclass(frozen=True)
class InferenceRule:
    head: tuple
    body: list[tuple]


    def __str__(self) -> str:
        if len(self.body) == 0:
            return str(self.head) + "."
        else:
            return str(self.head) + " :- " + ", ".join([(str(atom)) for atom in self.body]) + "."


    def get_all_variables(self) -> list[str]:
        variables = []

        for arg in self.head[1:]:
            if isinstance(arg, Variable):
                variables.append(arg.name)

        for atom in self.body:
            for arg in atom[1:]:
                if isinstance(arg, Variable):
                    variables.append(arg.name)

        return variables
