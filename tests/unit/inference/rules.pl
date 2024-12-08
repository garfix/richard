river('amazon').
river('brahma_putra').
parent('robert', 'martha').
parent('martha', 'william').
parent('william', 'beatrice').
parent('william', 'antonio').
grand_parent(X, Y) :- parent(X, Z), parent(Z, Y).
knows(A, "true") :- scoped(A).
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
