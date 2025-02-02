from dataclasses import dataclass, field


@dataclass(frozen=True)
class BlockResult:

    error_type: str
    error_args: list[str] = field(default_factory=list)


