from abc import abstractmethod

from richard.Model import Model


class SomeQueryOptimizer:
    @abstractmethod
    def optimize(self, composition: list[tuple], model: Model) -> list[tuple]:
        pass