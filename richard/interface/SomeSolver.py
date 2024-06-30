from abc import ABC, abstractmethod


class SomeSolver(ABC):

    @abstractmethod
    def solve_for(self, atoms: list[tuple], binding: dict, variable: str) -> list[dict]:
        pass

    @abstractmethod
    def solve(self, atoms: list[tuple], binding: dict) -> list[dict]:
        pass

