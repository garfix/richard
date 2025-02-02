from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProcessResult:

    products: list[any]
    error_type: str
    error_args: list[str] = field(default_factory=list)


