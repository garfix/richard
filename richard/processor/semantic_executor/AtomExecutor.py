from richard.core.Logger import Logger
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor
from richard.interface.SomeSemanticComposer import SomeSemanticComposer
from richard.core.Solver import Solver
from richard.type.OrderedSet import OrderedSet


class AtomExecutor(SomeProcessor):
    """
    Executes the function that forms the meaning of the sentence, and produces its result
    """

    composer: SomeSemanticComposer
    solver: Solver


    def __init__(self, composer: SomeSemanticComposer, solver: Solver) -> None:
        super().__init__()
        self.composer = composer
        self.solver = solver


    def get_name(self) -> str:
        return "Executor"


    def process(self, request: SentenceRequest) -> ProcessResult:
        composition = self.composer.get_composition(request)

        for inference in composition.inferences:
            self.solver.write_atom(inference)

        bindings = self.solver.solve(composition.get_semantics_last_iteration())
        return ProcessResult([bindings], "")


    def collect(self, tuples: list[tuple]) -> OrderedSet[dict]:
        pass


    def get_results(self, request: SentenceRequest) -> list:
        return request.get_current_product(self)


    def log_product(self, product: any, logger: Logger):
        logger.add(str(product))
