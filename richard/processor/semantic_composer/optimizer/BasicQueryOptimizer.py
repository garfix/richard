from richard.core.Model import Model
from richard.interface.SomeQueryOptimizer import SomeQueryOptimizer
from richard.processor.semantic_composer.optimizer.IsolateIndependentParts import IsolateIndependentParts
from richard.processor.semantic_composer.optimizer.FrontResolveName import FrontResolveName
from richard.processor.semantic_composer.optimizer.SortByCost import SortByCost


class BasicQueryOptimizer(SomeQueryOptimizer):
    model: Model


    def __init__(self, model: Model) -> None:
        self.model = model


    def optimize(self, semantics: list[tuple], root_variables: list[str]) -> tuple[str, list[tuple]]:
        semantics_iterations = []
        semantics_iterations.append(["Semantics", semantics])

        semantics = FrontResolveName().sort(semantics)
        semantics_iterations.append(["Names resolved", semantics])

        semantics = SortByCost().sort(semantics, self.model)
        semantics_iterations.append(["Sorted by cost", semantics])

        semantics = IsolateIndependentParts().isolate(semantics, root_variables)
        semantics_iterations.append(["Isolated", semantics])

        return semantics_iterations
