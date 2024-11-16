from richard.core.Logger import Logger
from richard.core.Model import Model
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor
from richard.core.Solver import Solver
from richard.processor.semantic_composer.SemanticComposerProduct import SemanticComposerProduct
from richard.processor.semantic_executor.AtomExecutorProduct import AtomExecutorProduct


class AtomExecutor(SomeProcessor):
    """
    Executes the function that forms the meaning of the sentence, and produces its result
    """

    composer: SomeProcessor
    model: Model


    def __init__(self, composer: SomeProcessor, model: Model) -> None:
        super().__init__()
        self.composer = composer
        self.model = model


    def get_name(self) -> str:
        return "Executor"


    def process(self, request: SentenceRequest) -> ProcessResult:
        incoming: SemanticComposerProduct = request.get_current_product(self.composer)
        solver = Solver(self.model, log_stats=request.logger.should_log_stats())

        # store the inferences in the sentence context
        for inference in incoming.inferences:
            solver.write_atom(inference)

        # perform executable atoms
        solver.solve(incoming.executable)

        bindings = solver.solve(incoming.get_semantics_last_iteration())
        product = AtomExecutorProduct(bindings, solver.stats)

        return ProcessResult([product], "")

