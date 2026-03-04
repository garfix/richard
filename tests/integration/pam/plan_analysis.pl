
# [['read-plan', ['planner', '?x'], ['object', '?y']]],
# [['goal', ['planner', '?x'],
#             ['objective', ['poss', ['actor', '?x'], ['object', '?y']]]], ['isa', 'book', '?y']]
goal(possess(S1, E1, E2)) => read_plan(S1, E1, E2).

# [['goal', ['planner', '?x'], ['objective', ['poss', ['actor', '?x'], ['object', '?y']]]]],
# [['take-plan', ['planner', '?x'], ['object', '?y']]]
take_plan(S1, E1, E2) => goal(possess(S1, E1, E2)).

# [['take-plan', ['planner', '?x'], ['object', '?y']]],
# [['grasp', ['actor', '?x'], ['object', '?y']]]
grasp(S1, E1, E2) => take_plan(S1, E1, E2).

