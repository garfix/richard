from abc import ABC, abstractmethod


class SomeSolver(ABC):
    @abstractmethod
    def solve(self, atoms: list[tuple], binding: dict) -> list[dict]:
        pass

