from dataclasses import dataclass


@dataclass(frozen=True)
class Composition:
    semantics: list[tuple]
    optimized_semantics: list[tuple]
    inferences: list[tuple]
    intents: list[str]
