part_of_n(A, B, N) :- part_of_n(A, C, N1), part_of_n(C, B, N2), multiply(N1, N2, N).
part_of_n(A, B, N1) :- isa(A, AA), part_of_n(AA, B, N1).

