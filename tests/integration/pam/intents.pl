intent_understand(Story) :-
    store(output_type('understood')), reify(Story, Reified), induce_facts(Reified), analyze_plans(Story).

intent_explanation(Question) :-
    store(output_type('question')).

