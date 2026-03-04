from richard.core.Model import Model
from richard.core.Solver import Solver
from richard.entity.ExecutionContext import ExecutionContext
from richard.entity.InferenceRule import InferenceRule
from richard.module.PlainReadWriteModule import PlainReadWriteModule
from richard.module.InferenceModule import InferenceModule


def match(pattern, sentence, binding: dict, deduction_rules: list[InferenceRule], context: ExecutionContext):
    model = Model([
        PlainReadWriteModule(sentence),
        InferenceModule(deduction_rules)
    ])
    solver = Solver(model)

    # print(sentence)
    results = solver.solve(pattern)
    return results[0] if len(results) > 0 else None
