# intent predicates

intent_understand(Story) :-
    store(output_type('understood')), reify(Story, Data), store(Data), analyze_plans(Story).

intent_question() :-
    store(output_type('question')).


