from richard.core.Model import Model
from richard.core.Solver import Solver
from richard.entity.ExecutionContext import ExecutionContext
from richard.entity.InferenceRule import InferenceRule
from richard.module.PlainReadWriteModule import PlainReadWriteModule
from richard.module.InferenceModule import InferenceModule


def match(pattern, current_subject, binding: dict, deduction_rules: list[InferenceRule], context: ExecutionContext, sentence):
    model = Model([
        PlainReadWriteModule(sentence),
        PlainReadWriteModule(current_subject),
        InferenceModule(deduction_rules)
    ])
    # print()
    # print('sentence', sentence)
    # print('current_subject', current_subject)
    solver = Solver(model)

    results = solver.solve(pattern)
    # results = context.solver.solve(pattern)

    return results[0] if len(results) > 0 else None
