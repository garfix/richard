from abc import ABC, abstractmethod


class SomeSolver(ABC):

    @abstractmethod
    def solve(self, atoms: list[tuple]) -> list[dict]:
        pass


    # Same as `solve` but returns the first result, or None
    def find_first(self, atoms: list[tuple], binding: dict = {}) -> dict|None:
        result = self.solve(atoms)
        return result[0] if len(result) > 0 else None


    @abstractmethod
    def write_atoms(self, atoms: list[tuple]):
        pass


    @abstractmethod
    def write_atom(self, atom: tuple):
        pass
