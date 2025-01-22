# sentence-level predicates

# teach
sentence_tell(Atoms) :- store(Atoms), store(output_type('ok')).
sentence_learn(Head, Body) :- learn_rule(Head, Body), store(output_type('ok')).

# check
sentence_check(Truth) :- store(output_type(Truth)).

