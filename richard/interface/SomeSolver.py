from abc import ABC, abstractmethod


class SomeSolver(ABC):

    @abstractmethod
    def solve(self, atoms: list[tuple], binding: dict = {}) -> list[dict]:
        pass


    def solve1(self, atoms: list[tuple], binding: dict = {}) -> dict|None:
        result = self.solve(atoms, binding)
        return result[0] if len(result) > 0 else None


    @abstractmethod
    def write_atom(self, atom: tuple):
        pass
