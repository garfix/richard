from dataclasses import dataclass

from richard.core.atoms import format_value


@dataclass(frozen=True)
class Composition:
    semantics: list[tuple]
    optimized_semantics: list[tuple]
    inferences: list[tuple]
    return_variables: list[str]


    def __str__(self) -> str:
        s = "Semantics:\n" + format_value(self.semantics)
        if self.optimized_semantics != self.semantics:
            s += "\n\nOptimized:\n" + format_value(self.optimized_semantics)
        if self.inferences:
            s += "\n\nInferences:\n\n" + str(self.inferences)
        return s
