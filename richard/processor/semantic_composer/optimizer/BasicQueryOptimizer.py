from richard.Model import Model
from richard.processor.semantic_composer.optimizer.SortByCost import SortByCost


class BasicQueryOptimizer:
    def optimize(self, composition: list[tuple], model: Model) -> list[tuple]:
        # composition = SortByCost().sort(composition, model)
        return composition
    
