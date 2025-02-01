from dataclasses import dataclass
from richard.core.atoms import get_atoms_variables


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
        variables.extend(get_atoms_variables(self.head))
        variables.extend(get_atoms_variables(self.body))

        return variables
