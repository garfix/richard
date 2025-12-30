
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor
from richard.processor.semantic_composer.SemanticComposerProduct import SemanticComposerProduct


class GoalUnderstander(SomeProcessor):
    """
    Infers the goals and plans of the human.
    """

    composer: SomeProcessor


    def __init__(self, composer: SomeProcessor) -> None:
        super().__init__()
        self.composer = composer


    def get_name(self) -> str:
        return "GoalUnderstander"


    def process(self, request: SentenceRequest) -> ProcessResult:
        incoming: SemanticComposerProduct = request.get_current_product(self.composer)
        # content = incoming.get_semantics_last_iteration()

        # todo process this content line by line

        active = True
        # main loop (p. 293)
        while active:
            active = False

        return ProcessResult(products=[incoming], error_type="")
