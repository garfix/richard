# implicit knowledge
recognize_plan(Atoms) :- Atoms = resolve_name('John', X), store(male(X), person(X)).

# FIND-OUT-REQ
# a person who is lost, has the goal of knowing where they are
recognize_plan(Atoms) :- Atoms = lost(A), store(
    goal_episode(
        goal_form(
            goal(
                know(A,
                    location(A, "?"))),
            source("?")),
        attempts())).

