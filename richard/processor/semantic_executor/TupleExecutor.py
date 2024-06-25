from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor
from richard.interface.SomeSemanticComposer import SomeSemanticComposer
from richard.Solver import Solver
from richard.type.OrderedSet import OrderedSet


class TupleExecutor(SomeProcessor):
    """
    Executes the function that forms the meaning of the sentence, and produces its result
    """
    
    composer: SomeSemanticComposer
    solver: Solver


    def __init__(self, composer: SomeSemanticComposer, solver: Solver) -> None:
        super().__init__()
        self.composer = composer    
        self.solver = solver

    
    def process(self, request: SentenceRequest) -> ProcessResult:
        atoms = self.composer.get_tuples(request)
        bindings = self.solver.solve(atoms)       
        return ProcessResult([bindings], "", [])
    

    def collect(self, tuples: list[tuple]) -> OrderedSet[dict]:
        pass


    def get_results(self, request: SentenceRequest) -> list:
        return request.get_current_product(self)
