from dataclasses import dataclass


@dataclass(frozen=True)
class SemanticComposerProduct:
    semantics_iterations: dict[str, list[tuple]]
    inferences: list[tuple]
    return_variables: list[str]


    def get_semantics_last_iteration(self):
        semantics = None
        for sem in self.semantics_iterations.values():
            semantics = sem
        return semantics
