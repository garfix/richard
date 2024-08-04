from abc import abstractmethod


class SomeQueryOptimizer:
    @abstractmethod
    def optimize(self, composition: list[tuple]) -> list[tuple]:
        pass