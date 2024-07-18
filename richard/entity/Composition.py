from dataclasses import dataclass


@dataclass(frozen=True)
class Composition:
    semantics: callable
    inferences: list[tuple]
    intents: list[str]
