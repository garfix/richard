from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.core.atoms import format_value
from richard.interface.Product import SomeProduct

@dataclass(frozen=True)
class SemanticComposerProduct(SomeProduct):
    semantics_iterations: dict[str, list[tuple]]
    inferences: list[tuple]
    executable: callable
    return_variables: list[str]


    def get_semantics_last_iteration(self):
        semantics = None
        for sem in self.semantics_iterations.values():
            semantics = sem
        return semantics


    def log(self, logger: Logger):
        logger.add_subheader("Executable")
        logger.add(format_value(self.executable))
        logger.add_subheader("Inferences")
        logger.add(format_value(self.inferences))
        logger.add_subheader("Return variables")
        logger.add(", ".join(self.return_variables))

        prev = None
        for description, value in self.semantics_iterations.items():
            if value != prev:
                logger.add_subheader(description)
                logger.add(format_value(value).strip())
                prev = value


    def get_output(self) -> any:
        return self.get_semantics_last_iteration()

