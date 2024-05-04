from dataclasses import dataclass
from .Process import Process

@dataclass(frozen=True)
class Pipeline:
    processes: list[Process]
