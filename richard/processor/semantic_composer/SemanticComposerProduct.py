from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.core.atoms import format_value
from richard.interface.Product import SomeProduct
from richard.processor.semantic_composer.SemanticSentence import SemanticSentence

@dataclass(frozen=True)
class SemanticComposerProduct(SomeProduct):
    sentences: list[SemanticSentence]

    def log(self, logger: Logger):
        for sentence in self.sentences:
            sentence.log(logger)


    def get_output(self) -> any:
        return list(map(lambda s: s.get_semantics_last_iteration(), self.sentences))

