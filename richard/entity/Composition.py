from dataclasses import dataclass


@dataclass(frozen=True)
class Composition:
    semantics: list[tuple]
    optimized_semantics: list[tuple]
    inferences: list[tuple]


    def __str__(self) -> str:
        s = "Semantics:\n" + self.format_value(self.semantics)
        if self.optimized_semantics != self.semantics:
            s += "\n\nOptimized:\n" + self.format_value(self.optimized_semantics)
        if self.inferences:
            s += "\n\nInferences:\n\n" + str(self.inferences)
        return s
    

    def format_value(self, value: any, indent: str = "\n") -> str:
        if isinstance(value, tuple):
            text = indent + "("
            sep = ""
            for element in value:
                text += sep + self.format_value(element, indent + "    ")
                sep = ", "
            text += ")"
        elif isinstance(value, list):
            text = indent + "["
            for element in value:
                text += self.format_value(element, indent + "    ")
            text += indent + "]"
        elif isinstance(value, str):
            text = "'" + value + "'"
        else:
            text = str(value)
        return text
    