# implicit knowledge
recognize_plan(Atoms) :- Atoms = resolve_name('John', X), store(male(X), person(X)).

# FIND-OUT-REQ
# a person who is lost, has the goal of knowing where they are
# TODO: this is not right
recognize_plan(Atoms) :- Atoms = lost(A), store(goal('know')).
# recognize_plan(Atoms) :- Atoms = lost(A), store(goal(know(A, location(A, L)))).
