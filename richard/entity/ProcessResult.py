from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessResult:

    products: list[any]
    error: str
    

