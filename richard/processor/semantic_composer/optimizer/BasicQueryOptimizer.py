from richard.Model import Model
from richard.interface.SomeQueryOptimizer import SomeQueryOptimizer
from richard.processor.semantic_composer.optimizer.IsolateIndependentParts import IsolateIndependentParts
from richard.processor.semantic_composer.optimizer.FrontResolveName import FrontResolveName
from richard.processor.semantic_composer.optimizer.SortByCost import SortByCost


class BasicQueryOptimizer(SomeQueryOptimizer):
    model: Model


    def __init__(self, model: Model) -> None:
        self.model = model


    def optimize(self, atoms: list[tuple], root_variables: list[str]) -> list[tuple]:
        atoms = FrontResolveName().sort(atoms)
        atoms = SortByCost().sort(atoms, self.model)
        atoms = IsolateIndependentParts().isolate(atoms, root_variables)
        return atoms

