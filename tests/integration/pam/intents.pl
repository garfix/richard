# intent predicates

intent_understood() :-
    store(output_type('understood')).

intent_question() :-
    store(output_type('question')).
