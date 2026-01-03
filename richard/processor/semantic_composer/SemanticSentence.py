from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.core.atoms import format_value


@dataclass(frozen=True)
class SemanticSentence:
    semantics_iterations: tuple[str, list[tuple]]
    inferences: list[tuple]
    executable: callable
    return_variables: list[str]


    def get_semantics_last_iteration(self):
        semantics = None
        for (description, value) in self.semantics_iterations:
            semantics = value
        return semantics


    def log(self, logger: Logger):
        logger.add_subheader("Executable")
        logger.add(format_value(self.executable))
        logger.add_subheader("Inferences")
        logger.add(format_value(self.inferences))
        logger.add_subheader("Return variables")
        logger.add(", ".join(self.return_variables))

        prev = None
        for (description, value) in self.semantics_iterations:
            if value != prev:
                logger.add_subheader(description)
                logger.add(format_value(value).strip())
                prev = value
