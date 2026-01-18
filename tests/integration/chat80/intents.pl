# intent predicates

optimize(SemIn, SemOut) :- optimize_frontize(SemIn, Sem2), optimize_cost_sort(Sem2, Sem3), optimize_isolate(Sem3, SemOut).

intent_list(E1, Sem) :-
    optimize(Sem, SemOpt),
    find_all(E1, SemOpt, Elements),
    store(output_type('list'), output_list(Elements)).

intent_table(Variables, Units, Body) :-
    optimize(Body, SemOpt),
    find_all(Variables, SemOpt, Results),
    store(output_type('table'), output_table(Results, Units)).

intent_yn(Body) :- (
    optimize(Body, SemOpt),
    scoped(SemOpt),  store(output_type('yes'))
;   store(output_type('no'))
).

intent_value(Variable, Sem) :-
    optimize(Sem, SemOpt),
    find_one(Variable, SemOpt, Result),
    store(output_type('value'), output_value(Result)).

intent_value_with_unit(Variable, Unit, Sem) :-
    optimize(Sem, SemOpt),
    find_one(Variable, SemOpt, Result),
    store(output_type('value_with_unit'), output_value_with_unit(Result, Unit)).

intent_close_conversation() :-
    store(output_type('close_conversation')).
