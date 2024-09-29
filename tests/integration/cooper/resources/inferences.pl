knows(A, "true") :- isolated(A).
knows(A, "false") :- negate(A).
knows(A, "unknown") :- not(isolated(A)), not(negate(A)).
