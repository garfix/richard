# intent predicates

intent_list(E1, Sem) :-
    find_all(E1, Sem, Elements),
    store(output_type('list'), output_list(Elements)).

intent_table(Variables, Units, Body) :-
    find_all(Variables, Body, Results),
    store(output_type('table'), output_table(Results, Units)).

intent_yn(Body) :- (
    scoped(Body),  store(output_type('yes'))
;   store(output_type('no'))
).

intent_value(Variable, Sem) :-
    find_one(Variable, Sem, Result),
    store(output_type('value'), output_value(Result)).

intent_value_with_unit(Variable, Unit, Sem) :-
    find_one(Variable, Sem, Result),
    store(output_type('value_with_unit'), output_value_with_unit(Result, Unit)).

intent_close_conversation() :-
    store(output_type('close_conversation')).
