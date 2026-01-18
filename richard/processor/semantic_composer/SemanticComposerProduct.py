from dataclasses import dataclass
from richard.core.Logger import Logger
from richard.interface.SomeProduct import SomeProduct
from richard.processor.semantic_composer.SemanticSentence import SemanticSentence

@dataclass(frozen=True)
class SemanticComposerProduct(SomeProduct):
    sentences: list[SemanticSentence]

    def log(self, logger: Logger):
        for sentence in self.sentences:
            sentence.log(logger)


    def get_output(self) -> any:
        return list(map(lambda s: s.semantics, self.sentences))

