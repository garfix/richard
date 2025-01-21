# sentence predicates

sentence_list(E1, Sem) :-
    find_all(E1, Sem, Elements), store(output_type('list'), output_list(Elements)).

sentence_table(Variables, Units, Body) :-
    find_all(Variables, Body, Results),
    store(output_type('table'), output_table(Results, Units)).



# other predicates

in(A, B) :- contains(B, A).
in(A, B) :- contains(C, A), in(C, B).
