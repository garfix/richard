from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeModel import SomeModel
from richard.interface.SomeProcessor import SomeProcessor
from richard.core.Solver import Solver
from richard.processor.semantic_composer.SemanticComposerProduct import SemanticComposerProduct
from richard.processor.semantic_executor.AtomExecutorProduct import AtomExecutorProduct


class AtomExecutor(SomeProcessor):
    """
    Executes the function that forms the meaning of the sentence, and produces its result
    """

    composer: SomeProcessor
    model: SomeModel


    def __init__(self, composer: SomeProcessor, model: SomeModel) -> None:
        super().__init__()
        self.composer = composer
        self.model = model


    def get_name(self) -> str:
        return "Executor"


    def process(self, incoming: SemanticComposerProduct) -> ProcessResult:
        sentences = incoming.sentences

        products = []
        for sentence in sentences:

            solver = Solver(self.model, sentence)

            # store the inferences in the sentence context
            for inference in sentence.inferences:
                solver.write_atom(inference)

            bindings = solver.solve(sentence.semantics)

            product = AtomExecutorProduct(bindings)

            # todo: is this right?
            products = [product]

        return ProcessResult(products, "")

