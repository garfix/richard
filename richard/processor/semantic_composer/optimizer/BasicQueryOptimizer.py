from richard.Model import Model
from richard.interface.SomeQueryOptimizer import SomeQueryOptimizer
from richard.processor.semantic_composer.optimizer.FrontResolveName import FrontResolveName
from richard.processor.semantic_composer.optimizer.SortByCost import SortByCost


class BasicQueryOptimizer(SomeQueryOptimizer):
    model: Model


    def __init__(self, model: Model) -> None:
        self.model = model


    def optimize(self, composition: list[tuple]) -> list[tuple]:
        composition = FrontResolveName().sort(composition)
        composition = SortByCost().sort(composition, self.model)
        return composition
    
