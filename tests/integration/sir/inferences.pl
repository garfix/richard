# isa
proper_isa(A, B) :- isa(A, B).
proper_isa(A, B) :- isa(A, C), proper_isa(C, B).

# isa including identity
full_isa(A, A).
full_isa(A, B) :- proper_isa(A, B).
# equality: John is Jack
full_isa(A, B) :- identical(A, B).
full_isa(A, B) :- identical(B, A).
full_isa(A, B) :- identical(A, C), proper_isa(C, B).
full_isa(A, B) :- identical(C, A), proper_isa(C, B).
full_isa(A, B) :- identical(B, C), proper_isa(A, C).
full_isa(A, B) :- identical(C, B), proper_isa(A, C).

#own
# find generalizations of A, find specializations of B
proper_own(A, B) :- full_isa(A, AA), full_isa(BB, B), own(AA, BB).

# part-of
# find specializations of A, find generalizations of B
proper_part_of(A, B) :- full_isa(AA, A), full_isa(B, BB), part_of(AA, BB).
# part-of is transitive
proper_part_of(A, B) :- full_isa(A, AA), part_of(AA, C), proper_part_of(C, B).

# part-of with number
part_of_number(A, B, N) :- full_isa(AA, A), full_isa(B, BB), part_of(AA, BB), part_of_n(AA, BB, N).
# part-of is transitive
part_of_number(A, B, N) :- full_isa(B, BB), part_of(C, BB), part_of(A, C), part_of_n(C, BB, N1), part_of_number(A, C, N2), multiply(N1, N2, N).

# position
# left_of is transitive
left_of(A, B) :- context('question'), just_left_of(A, B).
left_of(A, B) :- context('question'), just_left_of(A, C), left_of(C, B).
left_of(A, B) :- context('question'), just_left_of(C, B), left_of(A, C).
# if A is part of B, it has the same position as B
# todo: can use `proper_part_of`
just_left_of(A, B) :- part_of(A, C), isa(D, C), just_left_of(D, B).
just_left_of(B, A) :- part_of(A, C), isa(D, C), just_left_of(B, D).
left_of(A, B) :- part_of(A, C), isa(D, C), left_of(D, B).
left_of(B, A) :- part_of(A, C), isa(D, C), left_of(B, D).


somewhere_left_of(A, B) :- left_of(A, B), not(just_left_of(A, B)).

check_claim(Atom) :- destructure(Atom, 'just_left_of', A, B), check_just_left_of(A, B).
check_claim(Atom) :- destructure(Atom, 'left_of', A, B), check_left_of(A, B).

# check if the position just left of A is not already occupied
# check if A not to the right of B
check_just_left_of(A, B) :- not(just_left_of(A, C)), not(left_of(B, A)).
# check if A not to the right of B
check_left_of(A, B) :- not(left_of(B, A)).
