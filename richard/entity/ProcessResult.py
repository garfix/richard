from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessResult:

    products: list[any]
    error_code: str
    error_args: list[str]
    

