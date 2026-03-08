
# [['goal', ['planner', '?x'],
#             ['objective', ['know', ['actor', '?x'],
#                                     ['fact', ['is', ['actor', 'restaurant'], ['prox', '?z']]]]]]],
# [['read-plan', ['planner', '?x'], ['object', '?w']], ['isa', 'restaurant-guide', '?w']]
read_plan(S1, E1, E2), restaurant_guide(E2) => goal(know(E1, fact(restaurant(E2), distance(E2, E3)))).

# [['goal', ['planner', '?x'], ['objective', ['enjoyment', ['actor', '?x']]]]],
# [['read-plan', ['planner', '?x'], ['object', '?w']], ['isa', 'book', '?w']]
read_plan(S1, E1, E2) => goal(enjoyment(E1)).

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





# read_plan() -> plan(read()) (?)
