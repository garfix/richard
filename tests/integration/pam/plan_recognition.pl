# FIND-OUT-REQ
# a person who is lost, has the goal of knowing where they are

recognize_plan(Atoms) :- Atoms = lost(A), store(goal('know')).
# recognize_plan(Atoms) :- Atoms = lost(A), store(goal(know(A, location(A, L)))).
# recognize_plan(Atoms) :- Atoms = lost(A), store(goal('location', A, L)))).
