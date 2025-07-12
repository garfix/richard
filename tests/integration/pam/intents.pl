# intent predicates

intent_understand(Story) :-
    store(output_type('understood')).

intent_question() :-
    store(output_type('question')).


