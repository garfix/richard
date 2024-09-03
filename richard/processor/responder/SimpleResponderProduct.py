from dataclasses import dataclass


@dataclass
class SimpleResponderProduct:
    output: str


    def __str__(self) -> str:
        return self.output
