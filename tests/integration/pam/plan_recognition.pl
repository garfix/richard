# implicit knowledge
recognize_plan(Atoms) :- Atoms = resolve_name("John", Id1),
    resolve_name("John", Id),
    store(
        name("John", Id), male(Id), person(Id)).

# FIND-OUT-REQ
# a person who is lost, has the goal of knowing where they are
# recognize_plan(Atoms) :- Atoms = lost(B), Atoms = resolve_name(Name, Id1), resolve_name(Name, A), store(
#     goal_episode(
#         goal_form(
#             goal(
#                 know(A,
#                     location(A, "?"))),
#             source("?")),
#         attempts())).

recognize_plan(Atoms) :- scoped(Atoms) = scoped(resolve_name(Name, B), lost(B)),
    resolve_name(Name, A),
    store(
        goal_episode(
            goal_form(
                goal(
                    know(A, Name,
                        location(A, "?"))),
                source("?")),
            attempts())).

