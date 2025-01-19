from richard.entity.Relation import Relation
from richard.module.BasicSentenceContext import BasicSentenceContext
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class WikidataSentenceContext(BasicSentenceContext):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("output_report", arguments=["report"]))

