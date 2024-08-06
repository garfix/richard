from richard.Model import Model
from richard.processor.semantic_composer.optimizer.SortByCost import SortByCost
from richard.processor.semantic_composer.optimizer.ReduceExistsFinds import ReduceExistsFinds


class BasicQueryOptimizer:
    def optimize(self, composition: list[tuple], model: Model) -> list[tuple]:
        # composition = ReduceExistsFinds().reduce(composition)
        # composition = SortByCost().sort(composition, model)
        return composition
    
