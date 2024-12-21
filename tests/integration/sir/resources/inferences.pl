part_of_number(A, B, N) :- part_of(A, B), part_of_n(A, B, N).
part_of_number(A, B, N) :- part_of(C, B), part_of_n(C, B, N1), part_of_number(A, C, N2), multiply(N1, N2, N).
part_of_number(A, B, N) :- isa(A, AA), part_of_number(AA, B, N).
part_of_number(A, B, N) :- isa(B, BB), part_of_number(A, BB, N).
