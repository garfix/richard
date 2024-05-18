from richard.entity.BlockResult import BlockResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.ControlBlock import ControlBlock


class Succeed(ControlBlock):
    """
    This blocks is added as a terminal, so that the other blocks don't need to check if there's a next one
    """

    def process(self, request: SentenceRequest) -> BlockResult:
        return BlockResult('', [])

    