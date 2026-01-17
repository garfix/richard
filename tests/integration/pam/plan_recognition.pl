# FIND-OUT-REQ
# a person who is lost, has the goal of knowing where they are
recognize_plan(Atoms) :- Atoms = lost(A), store(goal(know(A, location(A)))).

# analyze() :- lost(A), store(goal(know(A, location(A))));

# analyze(lost(A)) :- store(goal(know(A, location(A))));

# recognize_plan() :- in_sentence(lost(A)), store(goal(know(A, location(A))));

