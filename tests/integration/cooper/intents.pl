# sentence-level predicates

# teach
intent_tell(Atoms) :- store(Atoms), store(output_type('ok')).
intent_learn(Head, Body) :- learn_rule(Head, Body), store(output_type('ok')).

# check
intent_check(Truth) :- store(output_type(Truth)).

