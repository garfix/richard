from richard.entity.Composition import Composition
from richard.interface.SomeProcessor import SomeProcessor


class SomeSemanticComposer(SomeProcessor):
    def get_composition() -> Composition:
        pass

