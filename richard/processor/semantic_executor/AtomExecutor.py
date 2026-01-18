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
        sentences = incoming.sentences

        products = []
        for sentence in sentences:

            solver = Solver(self.model, sentence, log_stats=request.logger.should_log_stats())

            # store the inferences in the sentence context
            for inference in sentence.inferences:
                solver.write_atom(inference)

            # perform executable atoms
            solver.solve(sentence.executable)

            bindings = solver.solve(sentence.get_semantics_last_iteration())

            product = AtomExecutorProduct(bindings, solver.stats)

            # todo: is this right?
            products = [product]

        return ProcessResult(products, "")

