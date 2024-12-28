# number objects involved in a part-of relationship
part_of_number(A, B, N) :- part_of(A, B), part_of_n(A, B, N).
part_of_number(A, B, N) :- part_of(C, B), part_of_n(C, B, N1), part_of_number(A, C, N2), multiply(N1, N2, N).
part_of_number(A, B, N) :- isa(A, AA), part_of_number(AA, B, N).
part_of_number(A, B, N) :- isa(B, BB), part_of_number(A, BB, N).

instance_of(A, A).
instance_of(A, B) :- instance_of_proper(A, B).
instance_of_proper(A, B) :- isa(A, B).
instance_of_proper(A, B) :- isa(A, C), instance_of_proper(C, B).

two_way_instance_of(A, B, 'yes') :- instance_of(A, B).
two_way_instance_of(A, B, 'sometimes') :- instance_of_proper(B, A).
