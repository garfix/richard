part_of_number(A, B, N) :- part_of_n(A, B, N).
part_of_number(A, B, N) :- part_of_n(A, C, N1), part_of_number(C, B, N2), multiply(N1, N2, N).
part_of_number(A, B, N) :- isa(A, AA), part_of_number(AA, B, N).
part_of_number(A, B, N) :- isa(B, BB), part_of_number(A, BB, N).
