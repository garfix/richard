from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.core.functions.terms import format_term


@dataclass(frozen=True)
class SemanticSentence:
    semantics: list[tuple]
    inferences: list[tuple]
    root_variables: list[str]


    def log(self, logger: Logger):
        logger.add_subheader("Semantics")
        logger.add(format_term(self.semantics))
        logger.add_subheader("Inferences")
        logger.add(format_term(self.inferences))
        logger.add_subheader("Return variables")
        logger.add(", ".join(self.root_variables))
