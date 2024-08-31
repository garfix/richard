from dataclasses import dataclass

from richard.core.atoms import format_value


@dataclass(frozen=True)
class Composition:
    semantics_iterations: dict[str, list[tuple]]
    inferences: list[tuple]
    return_variables: list[str]


    def __str__(self) -> str:
        result = []
        result.append("Inferences")
        result.append(str(self.inferences))
        result.append("Return variables")
        result.append(str(self.return_variables))

        for description, value in self.semantics_iterations.items():
            result.append(description)
            result.append(format_value(value))

        return "\n\n".join(result)


    def get_semantics_last_iteration(self):
        semantics = None
        for sem in self.semantics_iterations.values():
            semantics = sem
        return semantics
