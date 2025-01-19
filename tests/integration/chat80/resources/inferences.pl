# sentence predicates

sentence_names(Sem, E1) :-
    find_all(E1, Sem, Names), store(output_names(Names)).


# "dialog": [("format", "table"), ("format_table", e3, ''), ('format_table', e1, 'ksqmiles')],

sentence_table(Variables, Units, Body) :-
    find_all(Variables, Body, Results), store(output_type('table'), output_table(Results, Units)).



# other predicates

in(A, B) :- contains(B, A).
in(A, B) :- contains(C, A), in(C, B).
