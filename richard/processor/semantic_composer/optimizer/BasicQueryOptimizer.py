from richard.Model import Model
from richard.processor.semantic_composer.optimizer.FrontResolveName import FrontResolveName
from richard.processor.semantic_composer.optimizer.SortByCost import SortByCost


class BasicQueryOptimizer:
    def optimize(self, composition: list[tuple], model: Model) -> list[tuple]:
        composition = FrontResolveName().sort(composition)
        composition = SortByCost().sort(composition, model)
        return composition
    
