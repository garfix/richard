in(A, B) :- contains(B, A).
in(A, B) :- contains(C, A), in(C, B).
