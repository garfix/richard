# intent predicates

intent_understand(Story) :-
    store(output_type('understood')), store(Story), analyze_plans(Story).

intent_question() :-
    store(output_type('question')).


