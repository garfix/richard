
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor
from richard.processor.data.GoalEpisode import GoalEpisode
from richard.processor.data.Request import Request
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

        # find a matching request (in the discrimination net)
        request = self.find_matching_request() # p. 293

        # make a copy (p. 294)
        request_copy = self.resolve_request_references(request)

        # evaluate the action (p. 294)
        episode = self.evaluate_action(request_copy.action)




    def find_matching_request(self):
        pass


    def resolve_request_references(self, request: Request) -> Request:
        pass


    def evaluate_action(self, action: str) -> GoalEpisode:
        pass
