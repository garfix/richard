# recognize_plan(Atoms) :- Atoms = resolve_name("John", Id1),
#     resolve_name("John", Id),
#     store(
#         name("John", Id), male(Id), person(Id)).


# from richard.entity.Variable import Variable


# inductions = [
#     {
#         "if": ["resolve_name", ("John", Variable())]
#     }
# ]

name("John", Id1) => name("John", Id), male(Id), person(Id).
