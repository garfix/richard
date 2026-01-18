from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.core.atoms import format_value


@dataclass(frozen=True)
class SemanticSentence:
    semantics: list[tuple]
    inferences: list[tuple]
    executable: callable
    return_variables: list[str]


    def log(self, logger: Logger):
        logger.add_subheader("Semantics")
        logger.add(format_value(self.semantics))
        logger.add_subheader("Executable")
        logger.add(format_value(self.executable))
        logger.add_subheader("Inferences")
        logger.add(format_value(self.inferences))
        logger.add_subheader("Return variables")
        logger.add(", ".join(self.return_variables))
