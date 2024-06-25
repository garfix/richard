from abc import ABC, abstractmethod


class SomeSolver(ABC):
    @abstractmethod
    def solve(self, tuples: list[tuple], binding: dict = {}) -> list[dict]:
        pass

