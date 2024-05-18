from dataclasses import dataclass


@dataclass(frozen=True)
class BlockResult:

    error_code: str
    error_args: list[str]


