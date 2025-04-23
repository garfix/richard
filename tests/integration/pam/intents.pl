# intent predicates

intent_hello() :-
    store(output_type('hi')).

intent_list(E1, Sem) :-
    find_all(E1, Sem, Elements),
    store(output_type('list'), output_list(Elements)).
