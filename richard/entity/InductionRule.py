from dataclasses import dataclass
from richard.core.functions.atoms import get_variables


@dataclass(frozen=True)
class InductionRule:
    antecedent: list[tuple]
    consequent: list[tuple]


    def __str__(self) -> str:
        if len(self.antecedent) == 0:
            return str(self.antecedent) + "."
        else:
            return str(self.antecedent) + " => " + ", ".join([(str(atom)) for atom in self.consequent]) + "."


    def get_all_variables(self) -> list[str]:
        variables = []
        variables.extend(get_variables(self.antecedent))
        variables.extend(get_variables(self.consequent))

        return variables
